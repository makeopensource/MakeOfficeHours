import { validateSession } from "@/lib/helper/database-helper";
import { NextResponse, NextRequest } from "next/server";

export async function GET(request: NextRequest){
    try {
        const office_hours_id = request.nextUrl.searchParams.get("office_hours_id");
        const student_id = request.nextUrl.searchParams.get("student_id");
        if(!office_hours_id || !student_id){
            return NextResponse.json({ error: "Office hours id and student id are required" }, { status: 400 });
        }
        const {expired, is_valid} = await validateSession(office_hours_id, student_id);
        return NextResponse.json({expired, is_valid});
    } catch (error) {
        return NextResponse.json({ error: "Failed to validate session" }, { status: 500 });
    }
}