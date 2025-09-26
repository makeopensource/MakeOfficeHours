import jwt from "jsonwebtoken";
import crypto from "crypto";

import { NextResponse, NextRequest } from "next/server";
import { JWTApiError, JWTApiResponse, SupabaseJWTPayload } from "@/types/supabase-types";

export async function POST(req: NextRequest):Promise<NextResponse<JWTApiResponse | JWTApiError>> {
    try{
        const body = await req.json();
        const { access_token } = body;
        
        if (!access_token) {
            return NextResponse.json(
                { error: "Access token not provided" },
                { status: 400 }
            );
        }
        if (!process.env.AUTOLAB_USER_ENDPOINT) {
            return NextResponse.json(
                { error: "Missing required environment variables" },
                { status: 500 }
            );
        }
        
        // Getting user data from Autolab
        const autolabResponse = await fetch(process.env.AUTOLAB_USER_ENDPOINT, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${access_token}`,
            },
        });

        // Validating Autolab response

        if (!autolabResponse.ok) {
            const error = await autolabResponse.json();
            return NextResponse.json(
                { error: "Error while getting user data", details: error },
                { status: 500 }
            );
        }

        const userData = await autolabResponse.json();

        // Generating JWT payload
        const now = Math.floor(Date.now() / 1000)
        const jwtPayload: SupabaseJWTPayload = {
          sub: userData.email,
          email: userData.email,
          phone: "",
          aud: "authenticated",
          role: "authenticated",
          iat: now,
          exp: now + 2 * 60 * 60, // 2 hours
          aal: "aal1",
          session_id: crypto.randomUUID(),
        }

        if (!process.env.JWT_SECRET) {
            return NextResponse.json(
                { error: "Missing required environment variables" },
                { status: 500 }
            );
        }

        const supabase_jwt = jwt.sign(jwtPayload,process.env.JWT_SECRET as string);

        return NextResponse.json({supabase_jwt});


    }catch(error){
        console.error("Error generating JWT:", error)
        return NextResponse.json(
        {
            error: "Error while generating jwt",
            details: error instanceof Error ? error.message : "Unknown error",
        },
        { status: 500 },
        )
    }
    
}

