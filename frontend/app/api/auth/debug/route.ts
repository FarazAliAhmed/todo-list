import { NextResponse } from "next/server";
import { Pool } from "pg";

export async function GET() {
  try {
    const checks = {
      DATABASE_URL: !!process.env.DATABASE_URL,
      BETTER_AUTH_SECRET: !!process.env.BETTER_AUTH_SECRET,
      BETTER_AUTH_URL: process.env.BETTER_AUTH_URL,
      NODE_ENV: process.env.NODE_ENV,
    };

    // Test database connection
    let dbStatus = "not tested";
    let tables: string[] = [];
    
    if (process.env.DATABASE_URL) {
      try {
        const pool = new Pool({
          connectionString: process.env.DATABASE_URL,
          ssl: { rejectUnauthorized: false },
          max: 1,
        });

        await pool.query("SELECT NOW()");
        dbStatus = "connected";

        // Check for Better Auth tables
        const result = await pool.query(`
          SELECT table_name 
          FROM information_schema.tables 
          WHERE table_schema = 'public' 
          AND table_name IN ('user', 'session', 'account', 'verification')
        `);
        
        tables = result.rows.map(row => row.table_name);
        await pool.end();
      } catch (error: any) {
        dbStatus = `error: ${error.message}`;
      }
    }

    return NextResponse.json({
      checks,
      dbStatus,
      tables,
      timestamp: new Date().toISOString(),
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message, stack: error.stack },
      { status: 500 }
    );
  }
}
