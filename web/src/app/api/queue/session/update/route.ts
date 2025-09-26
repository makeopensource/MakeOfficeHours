import { updateSession } from "@/lib/helper/session-helper";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
    try {
        const { id, status } = await request.json();
        const data = await updateSession(id, status)
        return NextResponse.json({ message: "Session Updated", data: data });
    } catch (error) {
        return NextResponse.json({ error: "Failed to update session", details: error }, { status: 500 });
    }
}