"""
Test script to verify database connection.
Run this to ensure the database is accessible and configured correctly.
"""
import sys
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).parent))

from app.database import engine
from sqlmodel import text


def test_connection():
    """Test database connection and basic query."""
    try:
        print("Testing database connection...")
        print(f"Database URL: {engine.url}")

        with engine.connect() as conn:
            # Test basic query
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()

            if row and row[0] == 1:
                print("✓ Database connection successful!")

                # Get PostgreSQL version
                version_result = conn.execute(text("SELECT version()"))
                version = version_result.fetchone()[0]
                print(f"✓ PostgreSQL version: {version.split(',')[0]}")

                return True
            else:
                print("✗ Database connection failed: Unexpected result")
                return False

    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
