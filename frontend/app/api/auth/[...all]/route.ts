// Better Auth API route handler
// This handles all Better Auth endpoints: /api/auth/*

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
