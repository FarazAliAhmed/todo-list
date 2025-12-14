// API Client for backend communication
// Handles JWT token attachment and all task operations

import { ApiError, CreateTaskDto, Task, UpdateTaskDto } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Custom error class for API errors
 */
export class ApiClientError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiClientError";
    this.status = status;
    this.detail = detail;
  }
}

/**
 * Get JWT token from Better Auth session
 */
async function getAuthToken(): Promise<string | null> {
  try {
    // Get token from Better Auth session storage
    // Better Auth stores the session in localStorage or cookies
    const session = localStorage.getItem("better-auth.session_token");
    return session;
  } catch (error) {
    console.error("Error getting auth token:", error);
    return null;
  }
}

/**
 * Make an authenticated API request with retry logic
 */
async function fetchWithAuth(
  url: string,
  options: RequestInit = {},
  retries: number = 1
): Promise<Response> {
  const token = await getAuthToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  // Add existing headers
  if (options.headers) {
    const existingHeaders = new Headers(options.headers);
    existingHeaders.forEach((value, key) => {
      headers[key] = value;
    });
  }

  // Attach JWT token if available
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const config: RequestInit = {
    ...options,
    headers,
  };

  try {
    const response = await fetch(url, config);

    // If unauthorized and we have retries left, try once more
    if (response.status === 401 && retries > 0) {
      // Token might be expired, try to refresh or re-fetch
      await new Promise((resolve) => setTimeout(resolve, 100));
      return fetchWithAuth(url, options, retries - 1);
    }

    return response;
  } catch (error) {
    // Network error - retry if we have retries left
    if (retries > 0) {
      await new Promise((resolve) => setTimeout(resolve, 500));
      return fetchWithAuth(url, options, retries - 1);
    }
    // Throw a more descriptive network error
    throw new ApiClientError(
      0,
      "Network error: Unable to connect to the server. Please check your connection and try again."
    );
  }
}

/**
 * Handle API response and errors
 */
async function handleResponse<T>(response: Response): Promise<T> {
  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  const contentType = response.headers.get("content-type");
  const isJson = contentType?.includes("application/json");

  if (!response.ok) {
    let errorDetail = "An error occurred";

    if (isJson) {
      try {
        const errorData: ApiError = await response.json();
        errorDetail = errorData.detail || errorDetail;
      } catch {
        errorDetail = response.statusText || errorDetail;
      }
    } else {
      errorDetail = response.statusText || errorDetail;
    }

    throw new ApiClientError(response.status, errorDetail);
  }

  if (isJson) {
    return response.json();
  }

  return undefined as T;
}

/**
 * API Client interface
 */
export const api = {
  /**
   * Get all tasks for a user
   * @param userId - The user ID
   * @returns Promise<Task[]>
   */
  async getTasks(userId: string): Promise<Task[]> {
    const url = `${API_BASE_URL}/api/${userId}/tasks`;
    const response = await fetchWithAuth(url, { method: "GET" });
    return handleResponse<Task[]>(response);
  },

  /**
   * Create a new task
   * @param userId - The user ID
   * @param data - Task creation data
   * @returns Promise<Task>
   */
  async createTask(userId: string, data: CreateTaskDto): Promise<Task> {
    const url = `${API_BASE_URL}/api/${userId}/tasks`;
    const response = await fetchWithAuth(url, {
      method: "POST",
      body: JSON.stringify(data),
    });
    return handleResponse<Task>(response);
  },

  /**
   * Update an existing task
   * @param userId - The user ID
   * @param taskId - The task ID
   * @param data - Task update data
   * @returns Promise<Task>
   */
  async updateTask(
    userId: string,
    taskId: number,
    data: UpdateTaskDto
  ): Promise<Task> {
    const url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}`;
    const response = await fetchWithAuth(url, {
      method: "PUT",
      body: JSON.stringify(data),
    });
    return handleResponse<Task>(response);
  },

  /**
   * Delete a task
   * @param userId - The user ID
   * @param taskId - The task ID
   * @returns Promise<void>
   */
  async deleteTask(userId: string, taskId: number): Promise<void> {
    const url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}`;
    const response = await fetchWithAuth(url, {
      method: "DELETE",
    });
    return handleResponse<void>(response);
  },

  /**
   * Toggle task completion status
   * @param userId - The user ID
   * @param taskId - The task ID
   * @returns Promise<Task>
   */
  async toggleComplete(userId: string, taskId: number): Promise<Task> {
    const url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}/complete`;
    const response = await fetchWithAuth(url, {
      method: "PATCH",
    });
    return handleResponse<Task>(response);
  },
};

export default api;
