import os
from contextlib import contextmanager
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tasks_db")


@contextmanager
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                )
            """)
            # Seed data only if table is empty
            cur.execute("SELECT COUNT(*) FROM tasks")
            count = cur.fetchone()[0]
            if count == 0:
                cur.executemany(
                    "INSERT INTO tasks (title, done) VALUES (%s, %s)",
                    [
                        ("Learn FastAPI", False),
                        ("Build CRUD API", False),
                        ("Deploy to GitHub", False),
                    ],
                )
            conn.commit()


class TaskRepository:
    def get_all(self) -> List[dict]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
                return [dict(row) for row in cur.fetchall()]

    def get_by_id(self, task_id: int) -> Optional[dict]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def create(self, title: str) -> dict:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "INSERT INTO tasks (title, done) VALUES (%s, FALSE) RETURNING id, title, done",
                    (title.strip(),)
                )
                row = cur.fetchone()
                conn.commit()
                return dict(row)

    def update(self, task_id: int, title: Optional[str] = None, done: Optional[bool] = None) -> Optional[dict]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Check if task exists
                cur.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
                row = cur.fetchone()
                if not row:
                    return None

                # Build update query dynamically
                updates = []
                params = []
                if title is not None:
                    if not title.strip():
                        raise ValueError("Title cannot be empty")
                    updates.append("title = %s")
                    params.append(title.strip())
                if done is not None:
                    updates.append("done = %s")
                    params.append(done)

                if not updates:
                    return dict(row)

                params.append(task_id)
                query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s RETURNING id, title, done"
                cur.execute(query, params)
                row = cur.fetchone()
                conn.commit()
                return dict(row) if row else None

    def delete(self, task_id: int) -> bool:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                deleted = cur.rowcount > 0
                conn.commit()
                return deleted


# Initialize on import
init_db()