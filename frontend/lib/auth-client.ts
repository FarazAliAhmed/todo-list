// Client-side Better Auth utilities
// Use this in React components for authentication

import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  // Better Auth runs on the frontend (Next.js API routes)
  // NOT on the backend API
  // Use window.location.origin in browser, fallback to env var for SSR
  baseURL: typeof window !== 'undefined' 
    ? window.location.origin 
    : process.env.BETTER_AUTH_URL || "http://localhost:3000",
});

// Export hooks and methods for use in components
export const { useSession, signIn, signUp, signOut } = authClient;
