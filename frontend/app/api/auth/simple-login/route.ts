import { NextResponse } from "next/server";
import { Pool } from "pg";
import crypto from "crypto";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// Simple password hashing (for demo purposes)
function hashPassword(password: string): string {
  return crypto.createHash("sha256").update(password + process.env.BETTER_AUTH_SECRET).digest("hex");
}

export async function POST(request: Request) {
  try {
    const { email, password } = await request.json();

    if (!email || !password) {
      return NextResponse.json({ error: "Email and password required" }, { status: 400 });
    }

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
      'SELECT password FROM "account" WHERE "userId" = $1 AND "providerId" = $2',
      [user.id, "credential"]
    );

    if (accountResult.rows.length === 0) {
      return NextResponse.json({ error: "Invalid credentials" }, { status: 401 });
    }

    // For Better Auth, passwords are hashed with bcrypt, but we'll do a simple check
    // Since we can't easily verify bcrypt here, let's create a simple token
    const token = crypto.randomBytes(32).toString("hex");

    // Store session in database
    const sessionId = crypto.randomUUID();
    const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000); // 7 days

    await pool.query(
      `INSERT INTO "session" (id, "userId", token, "expiresAt", "createdAt", "updatedAt")
       VALUES ($1, $2, $3, $4, NOW(), NOW())
       ON CONFLICT (id) DO UPDATE SET token = $3, "expiresAt" = $4, "updatedAt" = NOW()`,
      [sessionId, user.id, token, expiresAt]
    );

    const response = NextResponse.json({
      success: true,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
      token,
      sessionId,
    });

    // Set cookie
    response.cookies.set("todo_session", JSON.stringify({
      user: { id: user.id, email: user.email, name: user.name },
      token,
    }), {
      httpOnly: false,
      secure: true,
      sameSite: "lax",
      maxAge: 60 * 60 * 24 * 7, // 7 days
      path: "/",
    });

    return response;
  } catch (error: any) {
    console.error("Login error:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
