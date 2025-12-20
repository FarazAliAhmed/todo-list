"use client";

import { useSession } from "@/lib/auth-client";
import { useRouter, usePathname } from "next/navigation";
import { useEffect } from "react";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

/**
 * ProtectedRoute component that redirects unauthenticated users to login
 * Wraps pages that require authentication
 */
export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { data: session, isPending, error } = useSession();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Log for debugging
    console.log("ProtectedRoute - isPending:", isPending, "session:", session, "error:", error);
    
    // Redirect to login if not authenticated and not loading
    if (!isPending && !session) {
      const redirectUrl = `/login?redirect=${encodeURIComponent(pathname)}`;
      router.push(redirectUrl);
    }
  }, [session, isPending, router, pathname, error]);

  // Show loading spinner while checking authentication
  if (isPending) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-sm text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Don't render if not authenticated (will redirect)
  if (!session) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-sm text-gray-600">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  // Render children if authenticated
  return <>{children}</>;
}
