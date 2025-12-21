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
 * Get JWT token from session cookie
 */
async function getAuthToken(): Promise<string | null> {
  try {
    // Get session from our app_session cookie
    const cookies = document.cookie.split(";");
    const sessionCookie = cookies.find(c => c.trim().startsWith("app_session="));
    
    if (sessionCookie) {
      const value = sessionCookie.split("=").slice(1).join("=");
      const parsed = JSON.parse(decodeURIComponent(value));
      // Return the token from the session
      return parsed?.token || null;
    }
    return null;
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

    // Don't treat 401 as session expired - backend auth is disabled
    // Just show the error message
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

  // ============ Chat API Methods ============

  /**
   * Send a chat message to the AI assistant
   * @param userId - The user ID
   * @param message - The user's message
   * @param conversationId - Optional existing conversation ID
   * @returns Promise with conversation_id, response, and tool_calls
   */
  async sendChatMessage(
    userId: string,
    message: string,
    conversationId?: number
  ): Promise<{
    conversation_id: number;
    response: string;
    tool_calls: Array<{
      tool_name: string;
      arguments: Record<string, unknown>;
      result: Record<string, unknown>;
    }>;
  }> {
    const url = `${API_BASE_URL}/api/${userId}/chat`;
    const response = await fetchWithAuth(url, {
      method: "POST",
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    });
    return handleResponse(response);
  },

  /**
   * Get all conversations for a user
   * @param userId - The user ID
   * @returns Promise with list of conversations
   */
  async getConversations(userId: string): Promise<{
    conversations: Array<{
      id: number;
      title: string;
      created_at: string;
      message_count: number;
    }>;
  }> {
    const url = `${API_BASE_URL}/api/${userId}/conversations`;
    const response = await fetchWithAuth(url, { method: "GET" });
    return handleResponse(response);
  },

  /**
   * Get a specific conversation with messages
   * @param userId - The user ID
   * @param conversationId - The conversation ID
   * @returns Promise with conversation details and messages
   */
  async getConversation(
    userId: string,
    conversationId: number
  ): Promise<{
    id: number;
    title: string;
    created_at: string;
    updated_at: string;
    messages: Array<{
      id: number;
      role: string;
      content: string;
      created_at: string;
    }>;
  }> {
    const url = `${API_BASE_URL}/api/${userId}/conversations/${conversationId}`;
    const response = await fetchWithAuth(url, { method: "GET" });
    return handleResponse(response);
  },
};

export default api;
