"use client";

import ProtectedRoute from "@/components/ProtectedRoute";
import TaskForm from "@/components/TaskForm";
import TaskList from "@/components/TaskList";
import { api, ApiClientError } from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/lib/toast-context";
import { CreateTaskDto, Task, UpdateTaskDto } from "@/lib/types";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

function TasksPageContent() {
  const router = useRouter();
  const { user } = useAuth();
  const { showSuccess, showError, showWarning } = useToast();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    if (user?.id) {
      loadTasks();
    }
  }, [user?.id]);

  const loadTasks = async () => {
    if (!user?.id) return;

    setIsLoading(true);
    setLoadError(null);

    try {
      const fetchedTasks = await api.getTasks(user.id);
      setTasks(fetchedTasks);
    } catch (err: any) {
      if (err instanceof ApiClientError) {
        if (err.status === 401) {
          showError("Session expired. Please log in again.");
          router.push("/login");
        } else {
          setLoadError(err.detail || "Failed to load tasks");
        }
      } else {
        setLoadError("An error occurred");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTask = async (data: CreateTaskDto) => {
    if (!user?.id) return;

    try {
      const newTask = await api.createTask(user.id, data);
      setTasks((prev) => [newTask, ...prev]);
      showSuccess("Task created!");
    } catch (err: any) {
      if (err instanceof ApiClientError) {
        showError(err.detail || "Failed to create task");
      }
      throw err;
    }
  };

  const handleUpdateTask = async (data: CreateTaskDto) => {
    if (!user?.id || !editingTask) return;

    try {
      const updatedTask = await api.updateTask(user.id, editingTask.id, {
        title: data.title,
        description: data.description,
      });
      setTasks((prev) => prev.map((t) => (t.id === updatedTask.id ? updatedTask : t)));
      setEditingTask(null);
      showSuccess("Task updated!");
    } catch (err: any) {
      if (err instanceof ApiClientError) {
        showError(err.detail || "Failed to update task");
      }
      throw err;
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!user?.id) return;

    try {
      await api.deleteTask(user.id, taskId);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
      if (editingTask?.id === taskId) setEditingTask(null);
      showSuccess("Task deleted!");
    } catch (err: any) {
      if (err instanceof ApiClientError) {
        showError(err.detail || "Failed to delete task");
      }
      throw err;
    }
  };

  const handleToggleComplete = async (taskId: number) => {
    if (!user?.id) return;

    try {
      const updatedTask = await api.toggleComplete(user.id, taskId);
      setTasks((prev) => prev.map((t) => (t.id === updatedTask.id ? updatedTask : t)));
    } catch (err: any) {
      if (err instanceof ApiClientError) {
        showError(err.detail || "Failed to update task");
      }
      throw err;
    }
  };

  /**
   * Start editing a task
   */
  const handleEditTask = (task: Task) => {
    setEditingTask(task);

    // Scroll to form
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  /**
   * Cancel editing
   */
  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
          <p className="mt-2 text-sm text-gray-600">
            Manage your tasks and stay organized
          </p>
        </div>

        {/* Load error with retry option */}
        {loadError && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <svg
                className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <div className="flex-1">
                <p className="text-sm font-medium text-red-800">{loadError}</p>
              </div>
            </div>
            <div className="mt-3 flex gap-3">
              <button
                onClick={loadTasks}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors"
              >
                Retry
              </button>
              <button
                onClick={() => setLoadError(null)}
                className="px-4 py-2 text-sm font-medium text-red-700 bg-white border border-red-300 rounded-md hover:bg-red-50 transition-colors"
              >
                Dismiss
              </button>
            </div>
          </div>
        )}

        {/* Task Form */}
        <div className="mb-8">
          <TaskForm
            onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
            editingTask={editingTask}
            onCancelEdit={handleCancelEdit}
          />
        </div>

        {/* Task List */}
        <TaskList
          tasks={tasks}
          isLoading={isLoading}
          onToggleComplete={handleToggleComplete}
          onEdit={handleEditTask}
          onDelete={handleDeleteTask}
        />
      </div>
    </div>
  );
}

export default function TasksPage() {
  return (
    <ProtectedRoute>
      <TasksPageContent />
    </ProtectedRoute>
  );
}
