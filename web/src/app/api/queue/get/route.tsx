import { getQueue, getQueueEntry } from "@/lib/helper/queue-helper";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request : NextRequest){
    try{
        const body = await request.json()
        const { office_hours_id } = body;
        const studentQueueData = await getQueue(office_hours_id);
        return NextResponse.json(studentQueueData);
    }catch(error){
        return NextResponse.json({error: "Error while fetching queue", details: error}, {status: 500});
    }
}