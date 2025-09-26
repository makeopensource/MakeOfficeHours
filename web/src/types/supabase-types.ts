export interface SupabaseJWTPayload {
    sub: string
    email: string
    phone: string
    aud: string
    role: string
    iat: number
    exp: number
    aal: string
    session_id: string
  }
  
  export interface JWTApiResponse {
    supabase_jwt: string
  }
  
  export interface JWTApiError {
    error: string
    details?: any
  }
  