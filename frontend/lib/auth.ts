// Better Auth configuration
import { betterAuth } from "better-auth";
import { Pool } from "pg";

// Validate DATABASE_URL
if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL environment variable is not set");
}

export const auth = betterAuth({
  // Database configuration - use PostgreSQL adapter
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: {
      rejectUnauthorized: false,
    },
  }),

  // Email and password authentication
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },

  // Secret for JWT signing
  secret: process.env.BETTER_AUTH_SECRET || "",

  // Base URL
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",

  // Session configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },

  // Advanced options
  advanced: {
    generateId: () => crypto.randomUUID(),
  },
});

// Export types
export type Session = typeof auth.$Infer.Session;
