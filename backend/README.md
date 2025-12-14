# Backend - FastAPI Todo Application

## Setup Instructions

### 1. Create Neon PostgreSQL Database

1. Go to [Neon Console](https://console.neon.tech/)
2. Sign up or log in
3. Create a new project
4. Copy the connection string (it will look like: `postgresql://user:password@host.neon.tech/dbname`)

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your Neon database connection string:

```
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
JWT_SECRET=your-secret-key-here
```

### 4. Test Database Connection

```bash
python test_connection.py
```

You should see:
```
✓ Database connection successful!
✓ PostgreSQL version: PostgreSQL 16.x
```

### 5. Run Database Migrations

```bash
python -m app.migrations.create_tables
```

This will create the `users` and `tasks` tables with appropriate indexes.

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `email` (VARCHAR(255), Unique)
- `password_hash` (VARCHAR(255))
- `name` (VARCHAR(255), Optional)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Tasks Table
- `id` (SERIAL, Primary Key)
- `user_id` (UUID, Foreign Key → users.id)
- `title` (VARCHAR(200))
- `description` (TEXT, Optional)
- `completed` (BOOLEAN, Default: false)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### Indexes
- `idx_tasks_user_id` (on user_id)
- `idx_tasks_completed` (on completed)
- `idx_tasks_user_completed` (on user_id, completed)

## Troubleshooting

### Connection Issues

If you get connection errors:
1. Verify your DATABASE_URL is correct
2. Ensure your Neon database is active (not suspended)
3. Check that SSL mode is enabled (`?sslmode=require`)
4. Verify your IP is allowed (Neon allows all IPs by default)

### Migration Issues

If migrations fail:
1. Ensure the database connection works (`python test_connection.py`)
2. Check that tables don't already exist
3. Verify you have write permissions on the database
