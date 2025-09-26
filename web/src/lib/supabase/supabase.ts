'use server'

import { createClient, SupabaseClient } from '@supabase/supabase-js'
import { NextResponse } from 'next/server'
import { cookies } from 'next/headers'
import { JWTApiResponse } from '@/types/supabase-types';

// let supabase: SupabaseClient | null = null;

// Cache for storing the current client and its associated JWT
let clientCache: {
  client: SupabaseClient
  jwt: string
  expiresAt: number
} | null = null


/**
 * Fetches a JWT token from the API, with caching via cookies
 */

export async function fetchSupabaseJWT(access_token: string): Promise<string> {
  try {
    const cookieStore = await cookies();
    const supabase_jwt = cookieStore.get("supabase_jwt");
    const supabase_jwt_expiry = cookieStore.get("supabase_jwt_expiry");

    // Check if we have a valid JWT in cookies
    if (supabase_jwt && supabase_jwt_expiry) {
      const expiryTime = Number.parseInt(supabase_jwt_expiry.value)
      const bufferTime = 5 * 60 * 1000 // 5 minutes buffer before expiry

      if (Date.now() < expiryTime - bufferTime) {
        return supabase_jwt.value
      }
    }

    // If no valid JWT in cookies, fetch a new one from the API
    const jwtResponse = await fetch(`${process.env.NEXTAUTH_URL}/api/jwt`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ access_token })
    });

    if (!jwtResponse.ok) {
      const error = await jwtResponse.json()
      throw new Error(`Failed to fetch JWT: ${error.error || "Unknown error"}`)
    }

    const jwtData: JWTApiResponse = await jwtResponse.json()
    

    // Calculate expiry time (2 hours from now)
    const expiryTime = Date.now() + 2 * 60 * 60 * 1000
    // Set the new JWT and expiry in cookies
    cookieStore.set("supabase_jwt", jwtData.supabase_jwt, {
      httpOnly: true,
      maxAge: 60 * 60 * 2, // 2 hours
      secure: process.env.NODE_ENV === "production",
      path: "/",
      sameSite: "strict"
    });

    cookieStore.set("supabase_jwt_expiry", expiryTime.toString(), {
      httpOnly: true,
      maxAge: 2 * 60 * 60, // 2 hours in seconds
      secure: process.env.NODE_ENV === "production",
      path: "/",
      sameSite: "strict",
    })

    return jwtData.supabase_jwt
  } catch (error) {
    console.error("Error fetching JWT:", error)
    throw new Error(`Failed to fetch JWT: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

/**
 * Creates a new Supabase client with the provided JWT token
 */

// export function createSupabaseClient(jwt_token: string): SupabaseClient {
//   try {
//     if (!process.env.SUPABASE_URL || !process.env.SUPABASE_KEY) {
//       throw new Error("Missing required Supabase environment variables")
//     }

//     // Initialize Supabase client with the JWT token
//     const client = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY, {
//       global: {
//         headers: {
//           Authorization: `Bearer ${jwt_token}`,
//         },
//       },
//       realtime: {
//         params: {
//           eventsPerSecond: 10,
//         },
//       },
//     })
  
//     // Set auth for realtime
//     client.realtime.setAuth(jwt_token)
  
//     return client
//   } catch (err) {
//     console.error("Failed to initialize Supabase client:", err);
//     throw err;
//   }
// }

/**
 * Decodes JWT to get expiry time (simple decode, no verification needed here)
 */

function getJWTExpiry(jwt: string): number {
  try {
    const payload = JSON.parse(atob(jwt.split(".")[1]))
    return payload.exp * 1000 // Convert to milliseconds
  } catch {
    return 0 // If we can't decode, assume expired
  }
}

/**
 * Gets or creates a Supabase client with proper caching and JWT management
 */
export async function getSupabaseClient(access_token: string): Promise<SupabaseClient> {
  try {
    // Check if we have a cached client and if it's still valid
    if (clientCache) {
      const jwtExpiry = getJWTExpiry(clientCache.jwt)
      const bufferTime = 5 * 60 * 1000 // 5 minutes buffer

      if (Date.now() < jwtExpiry - bufferTime) {
        return clientCache.client
      } else {
        // Clear expired cache
        clientCache = null
      }
    }

    // Fetch fresh JWT
    const jwt_token = await fetchSupabaseJWT(access_token)

    // Create new client
    // const client = createSupabaseClient(jwt_token)
    if (!process.env.NEXT_PUBLIC_SUPABASE_URL || !process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
      throw new Error("Missing required Supabase environment variables")
    }

    // Initialize Supabase client with the JWT token
    const client = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY, {
      global: {
        headers: {
          Authorization: `Bearer ${jwt_token}`,
        },
      },
      realtime: {
        params: {
          eventsPerSecond: 10,
        },
      },
    })
  
    // Set auth for realtime
    client.realtime.setAuth(jwt_token)

    // Cache the client with its JWT and expiry
    clientCache = {
      client,
      jwt: jwt_token,
      expiresAt: getJWTExpiry(jwt_token),
    }

    return client
  } catch (error) {
    console.error("Error getting Supabase client:", error)
    throw new Error(`Failed to initialize Supabase client: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

/**
 * Helper function to get a Supabase client for server actions/components
 * This is a convenience wrapper around getSupabaseClient
 */
export async function createServerSupabaseClient(access_token: string): Promise<SupabaseClient> {
  return getSupabaseClient(access_token)
}

// export const initialize = async (access_token: string): Promise<SupabaseClient> => {
//   try {
//     const jwtToken = await fetchSupabaseJWT(access_token); // Get or fetch JWT
//     const client = await initializeSupabaseClient(jwtToken); // Initialize Supabase client with JWT
//     return client;
//   } catch (err) {
//     console.error("Error initializing Supabase client:", err);
//     throw new Error("Failed to initialize Supabase client");
//   }
// }

// export const getSupabaseClient = async (access_token: string): Promise<SupabaseClient | null> => {
//   // If Supabase client isn't already initialized, initialize it
//   if (!supabase) {
//     console.log("Supabase client is not initialized, initializing... _");
//     supabase = await initialize(access_token); // Initialize Supabase with JWT
//   }

//   return supabase;
// }




