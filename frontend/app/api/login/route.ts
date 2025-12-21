import { NextResponse } from "next/server";
import { Pool } from "pg";
import crypto from "crypto";
import { SignJWT } from "jose";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

function hash(str: string): string {
  return crypto.createHash("sha256").update(str).digest("hex");
}

// Get JWT secret as Uint8Array for jose
function getJwtSecret(): Uint8Array {
  const secret = process.env.JWT_SECRET || process.env.BETTER_AUTH_SECRET || "default-secret";
  return new TextEncoder().encode(secret);
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

    // Generate JWT token for backend API
    const token = await new SignJWT({ sub: user.id, email: user.email })
      .setProtectedHeader({ alg: "HS256" })
      .setIssuedAt()
      .setExpirationTime("7d")
      .sign(getJwtSecret());

    // Create session with token
    const session = { 
      user: { id: user.id, email: user.email, name: user.name },
      token: token
    };
    
    const response = NextResponse.json({ success: true, ...session });
    
    response.cookies.set("app_session", JSON.stringify(session), {
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
