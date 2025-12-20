import { NextResponse } from "next/server";
import { Pool } from "pg";
import crypto from "crypto";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

// Simple password hashing
function hashPassword(password: string): string {
  return crypto.createHash("sha256").update(password + (process.env.BETTER_AUTH_SECRET || "secret")).digest("hex");
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
      return NextResponse.json({ error: "Invalid email or password" }, { status: 401 });
    }

    const user = userResult.rows[0];

    // Check password from account table
    const accountResult = await pool.query(
      'SELECT password FROM "account" WHERE "userId" = $1 AND "providerId" = $2',
      [user.id, "credential"]
    );

    if (accountResult.rows.length === 0) {
      return NextResponse.json({ error: "Invalid email or password" }, { status: 401 });
    }

    const storedPassword = accountResult.rows[0].password;
    const hashedInput = hashPassword(password);

    // Verify password
    if (storedPassword !== hashedInput) {
      return NextResponse.json({ error: "Invalid email or password" }, { status: 401 });
    }

    // Create session token
    const token = crypto.randomBytes(32).toString("hex");
    const sessionId = crypto.randomUUID();
    const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);

    // Store session
    await pool.query(
      `INSERT INTO "session" (id, "userId", token, "expiresAt", "createdAt", "updatedAt")
       VALUES ($1, $2, $3, $4, NOW(), NOW())`,
      [sessionId, user.id, token, expiresAt]
    );

    const sessionData = {
      user: { id: user.id, email: user.email, name: user.name },
      token,
    };

    const response = NextResponse.json({
      success: true,
      ...sessionData,
      sessionId,
    });

    // Set cookie
    response.cookies.set("todo_session", JSON.stringify(sessionData), {
      httpOnly: false,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 60 * 60 * 24 * 7,
      path: "/",
    });

    return response;
  } catch (error: any) {
    console.error("Login error:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
