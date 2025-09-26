'use client'

import { createClient, type SupabaseClient } from '@supabase/supabase-js'
import { getSession } from 'next-auth/react'

let clientCache: {
  client: SupabaseClient
  jwt: string
  expiresAt: number
} | null = null

function getJWTExpiry(jwt: string): number {
  try {
    const payload = JSON.parse(atob(jwt.split('.')[1]))
    return payload.exp * 1000
  } catch {
    return 0
  }
}

async function fetchJWT(access_token: string): Promise<string> {
  const res = await fetch('/api/jwt', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ access_token }),
  })

  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.error || 'JWT fetch failed')
  }

  const data = await res.json()
  return data.supabase_jwt
}

export async function getClientSupabaseClient(): Promise<SupabaseClient> {
    try {
        if (clientCache && Date.now() < clientCache.expiresAt - 5 * 60 * 1000) {
            return clientCache.client
        }
        const session = await getSession()
        if (!session?.user.accessToken) {
            throw new Error('No access token found')
        }
        const jwt_token = await fetchJWT(session?.user.accessToken)
        const exp = getJWTExpiry(jwt_token)
        
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
          expiresAt: exp,
        }
        
        return client
    } catch (error) {
        console.error("Error getting Supabase client:", error)
        throw new Error(`Failed to initialize Supabase client: ${error instanceof Error ? error.message : "Unknown error"}`)
    }
}
