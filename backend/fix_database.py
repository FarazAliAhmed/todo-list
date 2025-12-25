"""
Script to fix database foreign key constraints.
Run this once to remove foreign keys that prevent user-less operation.
"""
import os
import sys
from sqlalchemy import create_engine, text

def fix_database():
    """Drop all foreign key constraints from tables."""
    database_url = os.environ.get("DATABASE_URL")
    
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)
    
    print(f"Connecting to database...")
    engine = create_engine(database_url)
    
    # SQL commands to drop foreign keys
    commands = [
        "ALTER TABLE IF EXISTS conversations DROP CONSTRAINT IF EXISTS conversations_user_id_fkey;",
        "ALTER TABLE IF EXISTS messages DROP CONSTRAINT IF EXISTS messages_conversation_id_fkey;",
        "ALTER TABLE IF EXISTS messages DROP CONSTRAINT IF EXISTS messages_user_id_fkey;",
        "ALTER TABLE IF EXISTS tasks DROP CONSTRAINT IF EXISTS tasks_user_id_fkey;",
    ]
    
    try:
        with engine.connect() as conn:
            for cmd in commands:
                print(f"Executing: {cmd}")
                conn.execute(text(cmd))
                conn.commit()
            
            # Verify no foreign keys remain
            result = conn.execute(text("""
                SELECT 
                    conname AS constraint_name,
                    conrelid::regclass AS table_name,
                    confrelid::regclass AS referenced_table
                FROM pg_constraint 
                WHERE contype = 'f' 
                AND conrelid::regclass::text IN ('conversations', 'messages', 'tasks')
            """))
            
            remaining = list(result)
            if remaining:
                print("\nWARNING: Some foreign keys still remain:")
                for row in remaining:
                    print(f"  - {row}")
            else:
                print("\n✓ All foreign keys successfully removed!")
                
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    fix_database()
