# AI Rematch Prompt - Week 3

I used the following prompt to ask an AI to migrate the in-memory CRUD API to SQLite:

---

**Prompt:**

Migrate an in-memory FastAPI CRUD task API to SQLite database. The API has these endpoints:
- GET /tasks (list all)
- GET /tasks/{id} (get one)
- POST /tasks (create with title, returns 201)
- PUT /tasks/{id} (update title/done)
- DELETE /tasks/{id} (delete, returns 204)

Requirements:
- Use Python's built-in sqlite3 library
- Create tasks table with columns: id (INTEGER PRIMARY KEY AUTOINCREMENT), title (TEXT NOT NULL), done (INTEGER DEFAULT 0)
- Create table if not exists on startup
- Seed 3 example tasks ONLY when table is empty (count rows first)
- Use parameterized queries (?) for all SQL - no string concatenation
- Keep exact same request/response format and status codes (200, 201, 204, 400, 404)
- Return 404 with JSON error for unknown IDs
- Return 400 for missing/empty title
- Database file: tasks.db (created automatically)
- Server runs on port 8000

---