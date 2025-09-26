'use server'


import { authOptions } from "@/lib/auth/auth-option";
import { m } from "framer-motion";
import { getServerSession } from "next-auth";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
    try{
        const session = await getServerSession(authOptions);

        
        if(!session){
            return NextResponse.json({ message: "No session found" }, { status: 400 });
        }
        const access_token = session?.user?.accessToken;
        
        
        if(!access_token){
            return NextResponse.json({ message: "No access token found" }, { status: 400 });
        }
        return NextResponse.json({access_token});

    } catch (error) {
        return NextResponse.json({ error: 'Error occurred while retrieving access token', details: error }, { status: 500 });
    }
}