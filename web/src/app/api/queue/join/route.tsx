'use server'

import { JoinQueue } from "@/lib/helper/queue-helper";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { office_hours_id } = body;

    if (!office_hours_id) {
      return NextResponse.json(
        { error: "Office hours id is missing" },
        { status: 400 }
      );
    }

    const data = await JoinQueue(office_hours_id);
    return NextResponse.json(data);
  } catch (error : any) {
    return NextResponse.json(
      { error: "Error while joining queue", details: error.message },
      { status: 500 }
    );
  }
}
