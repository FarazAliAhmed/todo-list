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
    const { email, password, name } = await request.json();

    // Check if exists
    const existing = await pool.query('SELECT id FROM "user" WHERE email = $1', [email]);
    if (existing.rows.length > 0) {
      return NextResponse.json({ error: "Email already registered" }, { status: 400 });
    }

    // Create user
    const userId = crypto.randomUUID();
    await pool.query(
      'INSERT INTO "user" (id, email, name, "emailVerified", "createdAt", "updatedAt") VALUES ($1, $2, $3, false, NOW(), NOW())',
      [userId, email, name]
    );

    // Create account with password
    const accountId = crypto.randomUUID();
    const hashedPassword = hash(password);
    await pool.query(
      'INSERT INTO "account" (id, "userId", "accountId", "providerId", password, "createdAt", "updatedAt") VALUES ($1, $2, $3, $4, $5, NOW(), NOW())',
      [accountId, userId, email, "credential", hashedPassword]
    );

    // Create session
    const session = { user: { id: userId, email, name } };
    
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
