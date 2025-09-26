import { leaveQueue } from "@/lib/helper/queue-helper";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request : NextRequest){
    try {
        const body = await request.json()
        const {office_hours_id} = body;
        if(!office_hours_id){
            return NextResponse.json({error: "Office hours id is missing"}, {status: 400});
        }
        const leftQueue = await leaveQueue(office_hours_id);
        return NextResponse.json({leftQueue}, {status: 200});
        // if(leftQueue){
        //     return NextResponse.json({message: "User has left the queue", leftQueue : true}, {status: 200});
        // }
        // else{
        //     return NextResponse.json({message: "User is not in the queue", leftQueue : false}, {status: 200})
        // };
    } catch (error) {
        return NextResponse.json({error: "Error while removing the user from the queue", details: error}, {status: 500});
    }
}