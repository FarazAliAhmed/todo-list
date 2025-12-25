"use client";

import { CreateTaskDto, Task } from "@/lib/types";
import { useEffect, useState } from "react";

interface TaskFormProps {
  onSubmit: (data: CreateTaskDto) => Promise<void>;
  editingTask?: Task | null;
  onCancelEdit?: () => void;
}

export default function TaskForm({
  onSubmit,
  editingTask,
  onCancelEdit,
}: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<{
    title?: string;
    description?: string;
  }>({});

  // Populate form when editing
  useEffect(() => {
    if (editingTask) {
      setTitle(editingTask.title);
      setDescription(editingTask.description || "");
    } else {
      setTitle("");
      setDescription("");
    }
    setErrors({});
  }, [editingTask]);

  const validateForm = (): boolean => {
    const newErrors: { title?: string; description?: string } = {};

    // Title validation (1-200 chars)
    if (!title.trim()) {
      newErrors.title = "Title is required";
    } else if (title.length > 200) {
      newErrors.title = "Title must be 200 characters or less";
    }

    // Description validation (max 1000 chars)
    if (description && description.length > 1000) {
      newErrors.description = "Description must be 1000 characters or less";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || undefined,
      });

      // Clear form after successful submission (only if not editing)
      if (!editingTask) {
        setTitle("");
        setDescription("");
      }
      setErrors({});
    } catch (error) {
      console.error("Error submitting task:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = () => {
    setTitle("");
    setDescription("");
    setErrors({});
    if (onCancelEdit) {
      onCancelEdit();
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 md:p-6"
    >
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        {editingTask ? "Edit Task" : "Create New Task"}
      </h2>

      {/* Title input */}
      <div className="mb-4">
        <label
          htmlFor="title"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Title <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isSubmitting}
          className={`
            w-full px-3 py-2 border rounded-md shadow-sm
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            disabled:bg-gray-100 disabled:cursor-not-allowed
            text-black placeholder:text-gray-400
            ${errors.title ? "border-red-500" : "border-gray-300"}
          `}
          placeholder="Enter task title"
          maxLength={200}
          aria-invalid={!!errors.title}
          aria-describedby={errors.title ? "title-error" : undefined}
        />
        {errors.title && (
          <p id="title-error" className="mt-1 text-sm text-red-600">
            {errors.title}
          </p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          {title.length}/200 characters
        </p>
      </div>

      {/* Description input */}
      <div className="mb-4">
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 mb-1"
        >
          Description <span className="text-gray-400">(optional)</span>
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={isSubmitting}
          rows={3}
          className={`
            w-full px-3 py-2 border rounded-md shadow-sm
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            disabled:bg-gray-100 disabled:cursor-not-allowed
            resize-none
            text-black placeholder:text-gray-400
            ${errors.description ? "border-red-500" : "border-gray-300"}
          `}
          placeholder="Enter task description (optional)"
          maxLength={1000}
          aria-invalid={!!errors.description}
          aria-describedby={
            errors.description ? "description-error" : undefined
          }
        />
        {errors.description && (
          <p id="description-error" className="mt-1 text-sm text-red-600">
            {errors.description}
          </p>
        )}
        <p className="mt-1 text-xs text-gray-500">
          {description.length}/1000 characters
        </p>
      </div>

      {/* Action buttons */}
      <div className="flex gap-3 justify-end">
        {editingTask && onCancelEdit && (
          <button
            type="button"
            onClick={handleCancel}
            disabled={isSubmitting}
            className="
              px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300
              rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2
              focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed
              transition-colors duration-200
            "
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          disabled={isSubmitting}
          className="
            px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent
            rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2
            focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed
            transition-colors duration-200 flex items-center gap-2
          "
        >
          {isSubmitting && (
            <svg
              className="animate-spin h-4 w-4 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
          )}
          {isSubmitting
            ? editingTask
              ? "Updating..."
              : "Creating..."
            : editingTask
            ? "Update Task"
            : "Create Task"}
        </button>
      </div>
    </form>
  );
}
