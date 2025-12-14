"""
Database migration script to create initial tables.
Run this script to set up the database schema.
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.database import create_db_and_tables, engine
from app.models import User, Task
from sqlmodel import text


def create_indexes():
    """Create additional indexes for performance."""
    with engine.connect() as conn:
        # Index on tasks.user_id (already created by foreign key)
        # Index on tasks.completed
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed)"
        ))
        # Composite index on tasks(user_id, completed)
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_tasks_user_completed ON tasks(user_id, completed)"
        ))
        conn.commit()
        print("✓ Indexes created successfully")


def run_migration():
    """Run the migration to create all tables and indexes."""
    print("Creating database tables...")
    create_db_and_tables()
    print("✓ Tables created successfully")

    print("\nCreating indexes...")
    create_indexes()

    print("\n✓ Migration completed successfully!")


if __name__ == "__main__":
    run_migration()
