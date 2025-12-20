import { NextRequest, NextResponse } from "next/server";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

export async function GET(request: NextRequest) {
  try {
    const cookieValue = request.cookies.get("todo_session")?.value;
    
    if (!cookieValue) {
      return NextResponse.json({ session: null });
    }

    const session = JSON.parse(cookieValue);
    
    if (!session?.user?.id || !session?.token) {
      return NextResponse.json({ session: null });
    }

    // Verify session in database
    const result = await pool.query(
      `SELECT s.id, s."userId", s.token, s."expiresAt", u.email, u.name
       FROM "session" s
       JOIN "user" u ON s."userId" = u.id
       WHERE s."userId" = $1 AND s.token = $2 AND s."expiresAt" > NOW()`,
      [session.user.id, session.token]
    );

    if (result.rows.length === 0) {
      return NextResponse.json({ session: null });
    }

    const dbSession = result.rows[0];

    return NextResponse.json({
      session: {
        user: {
          id: dbSession.userId,
          email: dbSession.email,
          name: dbSession.name,
        },
        token: dbSession.token,
      },
    });
  } catch (error: any) {
    console.error("Session check error:", error);
    return NextResponse.json({ session: null, error: error.message });
  }
}
