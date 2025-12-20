"use client";

import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

interface User {
  id: string;
  email: string;
  name: string;
}

interface Session {
  user: User;
  token: string;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check localStorage for session
    const checkSession = () => {
      const stored = localStorage.getItem("todo_session");
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          if (parsed?.user?.id && parsed?.token) {
            setSession(parsed);
            setIsLoading(false);
            return;
          }
        } catch (e) {
          console.error("Failed to parse session:", e);
        }
      }
      
      // No valid session, redirect to login
      setIsLoading(false);
      const redirectUrl = `/login?redirect=${encodeURIComponent(pathname)}`;
      router.push(redirectUrl);
    };

    checkSession();
  }, [pathname, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-sm text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-sm text-gray-600">Redirecting to login...</p>
      </div>
    );
  }

  return <>{children}</>;
}
