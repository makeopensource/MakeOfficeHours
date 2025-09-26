import "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      userID: unknown;
      courses: string[];
      id: string;
      name: string;
      email: string;
      accessToken?: string;
      refreshToken?: string;
      expiresAt?: number;
    };
  }

  interface User {
    id: string;
    name: string;
    email: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    accessToken?: string;
    refreshToken?: string;
    expiresAt?: number;
  }
}
