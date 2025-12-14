// Better Auth configuration
import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Validate DATABASE_URL
if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL environment variable is not set");
}

// Create PostgreSQL connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false,
  },
  max: 10,
});

export const auth = betterAuth({
  // Database configuration
  database: {
    provider: "pg",
    url: process.env.DATABASE_URL,
  },

  // Email and password authentication
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },

  // Secret for JWT signing
  secret: process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET || "",

  // Base URL
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",

  // Session configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
});

// Export types
export type Session = typeof auth.$Infer.Session;
