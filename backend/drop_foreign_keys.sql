-- Drop all foreign key constraints from tables
-- This script removes foreign keys that prevent user-less operation

-- Drop foreign key from conversations table
ALTER TABLE IF EXISTS conversations 
DROP CONSTRAINT IF EXISTS conversations_user_id_fkey;

-- Drop foreign key from messages table (if any)
ALTER TABLE IF EXISTS messages 
DROP CONSTRAINT IF EXISTS messages_conversation_id_fkey;

ALTER TABLE IF EXISTS messages 
DROP CONSTRAINT IF EXISTS messages_user_id_fkey;

-- Drop foreign key from tasks table (if any)
ALTER TABLE IF EXISTS tasks 
DROP CONSTRAINT IF EXISTS tasks_user_id_fkey;

-- Verify no foreign keys remain
SELECT 
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    confrelid::regclass AS referenced_table
FROM pg_constraint 
WHERE contype = 'f' 
AND conrelid::regclass::text IN ('conversations', 'messages', 'tasks');
