import { getUserFromDatabase } from "@/lib/helper/database-helper"
import { NextRequest } from "next/server"
import { NextResponse } from "next/server"


export async function GET(request: NextRequest){
    try{
        const {searchParams} = new URL(request.url)
        const id = searchParams.get("id")
        if(!id){
            return NextResponse.json({error: "Id is required"}, {status: 400})
        }
        const user = await getUserFromDatabase(id)
        return NextResponse.json(user)
    }catch(error){
        return NextResponse.json({error: "Error while fetching user", details: error}, {status: 500})
    }
}   