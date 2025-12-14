// Client-side Better Auth utilities
// Use this in React components for authentication

import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  // Better Auth runs on the frontend (Next.js API routes)
  // NOT on the backend API
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
});

// Export hooks and methods for use in components
export const { useSession, signIn, signUp, signOut } = authClient;
