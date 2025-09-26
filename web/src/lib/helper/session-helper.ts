
import { getServerSession } from "next-auth";
import { getSupabaseClient } from "../supabase/supabase";
import { authOptions } from "../auth/auth-option";
import { NextResponse } from "next/server";

export async function updateSession(id: string, status: string) {
    try {
        const session = await getServerSession(authOptions);
        const access_token = session?.user?.accessToken;
        
        if (!access_token || !session) {
          throw new Error("Session is invalid or access token is missing");
        }
    
        const supabase = await getSupabaseClient(access_token);
        if (!supabase) {
          throw new Error("Supabase client is not initialized");
        }
        const { data, error } = await supabase
            .from('queue')
            .update({ status: status })
            .eq('id', id)
            .select()
            .single()
        if (error) {
            throw new Error("Failed to update session");
        }
        return data;
    } catch (error) {
        return NextResponse.json({ error: "Failed to update session", details: error }, { status: 500 });
    }
}