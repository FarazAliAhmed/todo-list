/**
 * Better Auth Database Migration Script
 * Run this to create Better Auth tables in your database
 */

import { auth } from "../lib/auth";

async function migrate() {
  console.log("Starting Better Auth database migration...");

  try {
    // Run Better Auth migrations
    await auth.api.migrate();

    console.log("✓ Better Auth tables created successfully");
    console.log("\nYou can now start the application with: npm run dev");
    process.exit(0);
  } catch (error) {
    console.error("✗ Migration failed:", error);
    process.exit(1);
  }
}

migrate();
