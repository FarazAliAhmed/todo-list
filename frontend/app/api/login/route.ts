import { NextResponse } from "next/server";
import { Pool } from "pg";
import crypto from "crypto";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

function hash(str: string): string {
  return crypto.createHash("sha256").update(str).digest("hex");
}

export async function POST(request: Request) {
  try {
    const { email, password } = await request.json();

    // Find user
    const userResult = await pool.query(
      'SELECT id, email, name FROM "user" WHERE email = $1',
      [email]
    );

    if (userResult.rows.length === 0) {
      return NextResponse.json({ error: "Invalid credentials" }, { status: 401 });
    }

    const user = userResult.rows[0];

    // Check password
    const accountResult = await pool.query(
      'SELECT password FROM "account" WHERE "userId" = $1',
      [user.id]
    );

    if (accountResult.rows.length === 0) {
      return NextResponse.json({ error: "Invalid credentials" }, { status: 401 });
    }

    const storedHash = accountResult.rows[0].password;
    const inputHash = hash(password);

    if (storedHash !== inputHash) {
      return NextResponse.json({ error: "Invalid credentials" }, { status: 401 });
    }

    // Create session
    const session = { user: { id: user.id, email: user.email, name: user.name } };
    
    const response = NextResponse.json({ success: true, ...session });
    
    response.cookies.set("app_session", JSON.stringify(session), {
      httpOnly: false,
      secure: false,
      sameSite: "lax",
      maxAge: 60 * 60 * 24 * 7,
      path: "/",
    });

    return response;
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
