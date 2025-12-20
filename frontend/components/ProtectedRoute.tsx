"use client";

import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    // Check cookie
    const checkAuth = () => {
      const cookies = document.cookie.split(";");
      const sessionCookie = cookies.find(c => c.trim().startsWith("app_session="));
      
      if (sessionCookie) {
        try {
          const value = sessionCookie.split("=").slice(1).join("=");
          const parsed = JSON.parse(decodeURIComponent(value));
          if (parsed?.user?.id) {
            setIsAuthenticated(true);
            return;
          }
        } catch (e) {
          console.error("Cookie parse error:", e);
        }
      }
      
      setIsAuthenticated(false);
    };

    // Small delay to ensure cookie is set
    setTimeout(checkAuth, 50);
  }, []);

  useEffect(() => {
    if (isAuthenticated === false) {
      router.push(`/login?redirect=${encodeURIComponent(pathname)}`);
    }
  }, [isAuthenticated, pathname, router]);

  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
