// Simple session management using cookies
import { cookies } from "next/headers";

const SESSION_COOKIE = "app_session";

export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Session {
  user: User;
}

// Server-side: Get session from cookie
export async function getServerSession(): Promise<Session | null> {
  try {
    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get(SESSION_COOKIE);
    
    if (!sessionCookie?.value) {
      return null;
    }
    
    return JSON.parse(sessionCookie.value);
  } catch {
    return null;
  }
}

// Client-side: Get session from cookie
export function getClientSession(): Session | null {
  if (typeof window === "undefined") return null;
  
  try {
    const cookies = document.cookie.split(";");
    const sessionCookie = cookies.find(c => c.trim().startsWith(`${SESSION_COOKIE}=`));
    
    if (!sessionCookie) return null;
    
    const value = sessionCookie.split("=")[1];
    return JSON.parse(decodeURIComponent(value));
  } catch {
    return null;
  }
}

// Client-side: Set session cookie
export function setClientSession(session: Session): void {
  if (typeof window === "undefined") return;
  
  const value = encodeURIComponent(JSON.stringify(session));
  document.cookie = `${SESSION_COOKIE}=${value}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
}

// Client-side: Clear session
export function clearClientSession(): void {
  if (typeof window === "undefined") return;
  document.cookie = `${SESSION_COOKIE}=; path=/; max-age=0`;
}
