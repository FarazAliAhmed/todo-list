import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Todo App</h1>
          <p className="text-gray-600">Phase II: Full-Stack Web Application</p>
        </div>

        <div className="space-y-4">
          <Link
            href="/login"
            className="block w-full py-3 px-4 text-center bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Login
          </Link>

          <Link
            href="/signup"
            className="block w-full py-3 px-4 text-center bg-gray-200 text-gray-900 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Sign Up
          </Link>

          <Link
            href="/tasks"
            className="block w-full py-3 px-4 text-center border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
          >
            View Tasks (Demo)
          </Link>
        </div>

        <p className="text-sm text-gray-500 text-center mt-6">
          Authentication and task management features will be implemented in
          subsequent tasks.
        </p>
      </div>
    </div>
  );
}
