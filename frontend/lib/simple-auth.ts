// Simple authentication using cookies directly
// This bypasses Better Auth completely

const AUTH_COOKIE_NAME = "todo_session";

export interface User {
  id: string;
  email: string;
  name: string;
}

export interface Session {
  user: User;
  token: string;
}

// Store session in localStorage and cookie
export function setSession(session: Session) {
  if (typeof window !== "undefined") {
    localStorage.setItem(AUTH_COOKIE_NAME, JSON.stringify(session));
    // Also set a cookie for SSR
    document.cookie = `${AUTH_COOKIE_NAME}=${encodeURIComponent(JSON.stringify(session))}; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
  }
}

// Get session from localStorage
export function getSession(): Session | null {
  if (typeof window !== "undefined") {
    const stored = localStorage.getItem(AUTH_COOKIE_NAME);
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch {
        return null;
      }
    }
  }
  return null;
}

// Clear session
export function clearSession() {
  if (typeof window !== "undefined") {
    localStorage.removeItem(AUTH_COOKIE_NAME);
    document.cookie = `${AUTH_COOKIE_NAME}=; path=/; max-age=0`;
  }
}

// Check if user is authenticated
export function isAuthenticated(): boolean {
  return getSession() !== null;
}
