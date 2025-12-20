"use client";

import { useEffect, useState } from "react";

export default function TestAuthPage() {
  const [session, setSession] = useState<string | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("todo_session");
    setSession(stored);
    setLoaded(true);
  }, []);

  const clearSession = () => {
    localStorage.removeItem("todo_session");
    setSession(null);
  };

  const testLogin = async () => {
    try {
      const response = await fetch("/api/auth/simple-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: "test@test.com",
          password: "test123",
        }),
      });
      const data = await response.json();
      alert("Login response: " + JSON.stringify(data, null, 2));
      
      if (data.user && data.token) {
        localStorage.setItem("todo_session", JSON.stringify({
          user: data.user,
          token: data.token,
        }));
        setSession(localStorage.getItem("todo_session"));
      }
    } catch (e: any) {
      alert("Error: " + e.message);
    }
  };

  const testSignup = async () => {
    const email = `test${Date.now()}@test.com`;
    try {
      const response = await fetch("/api/auth/simple-signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email,
          password: "test123",
          name: "Test User",
        }),
      });
      const data = await response.json();
      alert("Signup response: " + JSON.stringify(data, null, 2));
      
      if (data.user && data.token) {
        localStorage.setItem("todo_session", JSON.stringify({
          user: data.user,
          token: data.token,
        }));
        setSession(localStorage.getItem("todo_session"));
      }
    } catch (e: any) {
      alert("Error: " + e.message);
    }
  };

  if (!loaded) return <div>Loading...</div>;

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Auth Test Page</h1>
      
      <div className="mb-4 p-4 bg-gray-100 rounded">
        <h2 className="font-bold">Current Session:</h2>
        <pre className="text-xs overflow-auto mt-2">
          {session ? session : "No session found"}
        </pre>
      </div>

      <div className="space-x-4">
        <button
          onClick={testSignup}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          Test Signup
        </button>
        <button
          onClick={testLogin}
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          Test Login
        </button>
        <button
          onClick={clearSession}
          className="px-4 py-2 bg-red-600 text-white rounded"
        >
          Clear Session
        </button>
        <a
          href="/tasks"
          className="px-4 py-2 bg-purple-600 text-white rounded inline-block"
        >
          Go to Tasks
        </a>
      </div>
    </div>
  );
}
