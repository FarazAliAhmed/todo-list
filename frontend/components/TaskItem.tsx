"use client";

import { Task } from "@/lib/types";
import { useState } from "react";

interface TaskItemProps {
  task: Task;
  onToggleComplete: (taskId: number) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => Promise<void>;
}

export default function TaskItem({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskItemProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isToggling, setIsToggling] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      await onToggleComplete(task.id);
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    setIsDeleting(true);
    try {
      await onDelete(task.id);
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div
      className={`
        bg-white rounded-lg shadow-sm border border-gray-200 p-4
        transition-all duration-200 hover:shadow-md
        ${isDeleting ? "opacity-50" : ""}
      `}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox for completion status */}
        <button
          onClick={handleToggle}
          disabled={isToggling || isDeleting}
          className={`
            flex-shrink-0 mt-1 w-5 h-5 rounded border-2
            transition-all duration-200
            ${
              task.completed
                ? "bg-green-500 border-green-500"
                : "border-gray-300 hover:border-green-400"
            }
            ${isToggling ? "opacity-50 cursor-wait" : "cursor-pointer"}
            disabled:cursor-not-allowed
            flex items-center justify-center
          `}
          aria-label={
            task.completed ? "Mark as incomplete" : "Mark as complete"
          }
        >
          {task.completed && (
            <svg
              className="w-3 h-3 text-white"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M5 13l4 4L19 7"></path>
            </svg>
          )}
        </button>

        {/* Task content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`
              text-base font-medium break-words
              ${task.completed ? "line-through text-gray-400" : "text-gray-900"}
            `}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`
                mt-1 text-sm break-words
                ${task.completed ? "text-gray-400" : "text-gray-600"}
              `}
            >
              {task.description}
            </p>
          )}
          <div className="mt-2 flex items-center gap-2 text-xs text-gray-400">
            <span>
              Created: {new Date(task.created_at).toLocaleDateString()}
            </span>
            {task.updated_at !== task.created_at && (
              <span>
                • Updated: {new Date(task.updated_at).toLocaleDateString()}
              </span>
            )}
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex-shrink-0 flex gap-2">
          <button
            onClick={() => onEdit(task)}
            disabled={isDeleting}
            className="
              p-2 text-blue-600 hover:bg-blue-50 rounded-md
              transition-colors duration-200
              disabled:opacity-50 disabled:cursor-not-allowed
            "
            aria-label="Edit task"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
          </button>
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="
              p-2 text-red-600 hover:bg-red-50 rounded-md
              transition-colors duration-200
              disabled:opacity-50 disabled:cursor-not-allowed
            "
            aria-label="Delete task"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
