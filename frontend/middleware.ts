import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Get the session from our custom cookie
  const sessionCookie = request.cookies.get("app_session");

  // Define public routes
  const publicRoutes = ["/", "/login", "/signup", "/test-auth"];
  const isPublicRoute = publicRoutes.includes(pathname);

  // Define protected routes
  const protectedRoutes = ["/tasks", "/chat"];
  const isProtectedRoute = protectedRoutes.some((route) =>
    pathname.startsWith(route)
  );

  // If trying to access a protected route without a session, redirect to login
  if (isProtectedRoute && !sessionCookie) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // If trying to access auth pages while logged in, redirect to tasks
  if ((pathname === "/login" || pathname === "/signup") && sessionCookie) {
    return NextResponse.redirect(new URL("/tasks", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!api|_next/static|_next/image|favicon.ico|.*\\..*|public).*)",
  ],
};
