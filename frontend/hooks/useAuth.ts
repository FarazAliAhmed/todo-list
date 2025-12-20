"use client";

import { useEffect, useState } from "react";

interface User {
  id: string;
  email: string;
  name: string;
}

interface Session {
  user: User;
}

export function useAuth() {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check cookie directly
    const checkSession = () => {
      try {
        const cookies = document.cookie.split(";");
        const sessionCookie = cookies.find(c => c.trim().startsWith("app_session="));
        
        if (sessionCookie) {
          const value = sessionCookie.split("=").slice(1).join("=");
          const parsed = JSON.parse(decodeURIComponent(value));
          setSession(parsed);
        } else {
          setSession(null);
        }
      } catch (e) {
        setSession(null);
      }
      setLoading(false);
    };

    checkSession();
  }, []);

  const logout = () => {
    document.cookie = "app_session=; path=/; max-age=0";
    setSession(null);
    window.location.href = "/login";
  };

  return { session, loading, logout, user: session?.user };
}
