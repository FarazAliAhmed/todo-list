import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const sessionCookie = request.cookies.get("app_session");
  
  if (!sessionCookie?.value) {
    return NextResponse.json({ session: null });
  }
  
  try {
    const session = JSON.parse(sessionCookie.value);
    return NextResponse.json({ session });
  } catch {
    return NextResponse.json({ session: null });
  }
}
