import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    service: 'todo-frontend',
    version: '3.0.0',
  });
}
