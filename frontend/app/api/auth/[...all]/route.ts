// Better Auth API route handler
// This handles all Better Auth endpoints: /api/auth/*

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";
import { NextRequest, NextResponse } from "next/server";

const handler = toNextJsHandler(auth);

export async function GET(req: NextRequest) {
  try {
    return await handler.GET(req);
  } catch (error: any) {
    console.error("Better Auth GET Error:", error);
    return NextResponse.json(
      { 
        error: error.message, 
        stack: error.stack,
        name: error.name 
      },
      { status: 500 }
    );
  }
}

export async function POST(req: NextRequest) {
  try {
    return await handler.POST(req);
  } catch (error: any) {
    console.error("Better Auth POST Error:", error);
    return NextResponse.json(
      { 
        error: error.message, 
        stack: error.stack,
        name: error.name 
      },
      { status: 500 }
    );
  }
}
