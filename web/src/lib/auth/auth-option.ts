import { NextAuthOptions } from "next-auth";
import { OAuthConfig } from "next-auth/providers/oauth";
import { getUserCoursesFromAutolab, getUserInfo } from "../helper/autolab-helper";
import { pushUserToDataBase } from "../helper/database-helper";

interface DbUser {
  id: string;
}

// Extend Session type to include error property
declare module "next-auth" {
  interface Session {
    error?: string;
  }
}

interface AutolabProfile {
    first_name: string;
    last_name: string;
    email: string;
  }
  

const autolabProvider: OAuthConfig<AutolabProfile> = {
    id: "autolab",
    name: "Autolab",
    type: "oauth",
    version: "2.0",
    authorization:{
        url: `${process.env.AUTOLAB_AUTHORIZE_ENDPOINT}`,
        params:{
            response_type: "code",
            scope: "user_info user_courses",
            client_id: process.env.AUTOLAB_CLIENT_ID,
            redirect_uri:process.env.AUTOLAB_REDIRECT_URI,
        }
    },
    token:`${process.env.AUTOLAB_TOKEN_ENDPOINT}`,
    userinfo:{
        url:`${process.env.AUTOLAB_USER_ENDPOINT}`,
    },
    clientId: process.env.AUTOLAB_CLIENT_ID,
    clientSecret: process.env.AUTOLAB_CLIENT_SECRET,
    profile: (profile) => {
        return {
            id: profile.email,
            name: `${profile.first_name} ${profile.last_name}`,
            email: profile.email,
        };
    },
}

// Refresh access token if expired
export async function refreshAccessToken(token: any) {
  try {
    const response = await fetch(process.env.AUTOLAB_TOKEN_ENDPOINT!, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        refresh_token: token.refreshToken,
        client_id: process.env.AUTOLAB_CLIENT_ID!,
        client_secret: process.env.AUTOLAB_CLIENT_SECRET!,
        scope: "user_info user_courses"
      }),
    })

    const refreshed = await response.json()

    if (!response.ok) {
      throw refreshed
    }

    return {
      ...token,
      accessToken: refreshed.access_token,
      refreshToken: refreshed.refresh_token ?? token.refreshToken,
      expiresAt: Math.floor(Date.now() / 1000) + (refreshed.expires_in ?? 3600),
    }
  } catch (error) {
    console.error("Error refreshing access token:", error)
    return {
      ...token,
      error: "RefreshAccessTokenError",
    }
  }
}

export const authOptions: NextAuthOptions = {
  providers: [autolabProvider],
  session: { 
    strategy: "jwt",
    maxAge: 60 * 60 * 3,
    updateAge: 60 * 15,
  },
  debug: true,
  callbacks: {
    async jwt({ token, account }) {
      const now = Math.floor(Date.now() / 1000) // in seconds

      if (account) {
        const userData = await getUserInfo({ access_token: account.access_token! })
        const dbUser = await pushUserToDataBase({
          name: `${userData.first_name} ${userData.last_name}`,
          email: userData.email,
          access_token: account.access_token!,
        }) as DbUser;

        const userCourses = await getUserCoursesFromAutolab({
          access_token: account.access_token!,
        })

        return {
          accessToken: account.access_token,
          refreshToken: account.refresh_token,
          expiresAt: account.expires_at ?? (now + 3600),
          userCourses,
          id: dbUser.id,
          name: userData.first_name + " " + userData.last_name,
          email: userData.email,
        }
      }

      // Token is still valid
      if (token.expiresAt && now < token.expiresAt - 60) {
        return token
      }

      // Token expired: refresh it
      return await refreshAccessToken(token)
    },

    async session({ session, token }) {
      session.user.accessToken = token.accessToken
      session.user.refreshToken = token.refreshToken
      session.user.expiresAt = token.expiresAt
      session.user.courses = token.userCourses as string[]
      session.user.id = token.id as string
      session.user.name = token.name as string
      session.user.email = token.email as string
      session.error = token.error as string // for front-end error handling
      return session
    },

    async redirect({ url, baseUrl }) {
      if (url === baseUrl || url === `${baseUrl}/`) return `${baseUrl}/dashboard`
      if (url.startsWith("/")) return `${baseUrl}${url}`
      if (new URL(url).origin === baseUrl) return url
      return baseUrl
    },
  },
  pages: {
    signOut: "/",
  },
};
