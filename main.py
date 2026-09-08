import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException, Request, Response

app = FastAPI(title="Task API", version="1.0")

DB_PATH = "tasks.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)
        # Seed data only if table is empty
        count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                [
                    ("Learn FastAPI", 0),
                    ("Build CRUD API", 0),
                    ("Deploy to GitHub", 0),
                ],
            )
            conn.commit()


init_db()


@app.get("/", summary="API info", description="Returns basic information about the API")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Health check", description="Returns the health status of the API")
async def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks", description="Returns a list of all tasks")
async def get_tasks():
    with get_db() as conn:
        rows = conn.execute("SELECT id, title, done FROM tasks").fetchall()
        return [{"id": row["id"], "title": row["title"], "done": bool(row["done"])} for row in rows]


@app.get("/tasks/{task_id}", summary="Get a task by ID", description="Returns a single task by its ID")
async def get_task(task_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@app.post("/tasks", status_code=201, summary="Create a new task", description="Creates a new task with the given title")
async def create_task(request: Request):
    body = await request.json()
    title = body.get("title")
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    
    with get_db() as conn:
        cursor = conn.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (title.strip(),))
        conn.commit()
        new_id = cursor.lastrowid
        row = conn.execute("SELECT id, title, done FROM tasks WHERE id = ?", (new_id,)).fetchone()
        return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@app.put("/tasks/{task_id}", summary="Update a task", description="Updates a task's title and/or done status")
async def update_task(task_id: int, request: Request):
    body = await request.json()
    title = body.get("title")
    done = body.get("done")
    
    if title is not None and (not title or not title.strip()):
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    with get_db() as conn:
        row = conn.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        new_title = title.strip() if title is not None else row["title"]
        new_done = 1 if done is not None and done else (0 if done is not None and not done else row["done"])
        
        conn.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (new_title, new_done, task_id))
        conn.commit()
        
        row = conn.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)).fetchone()
        return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task", description="Deletes a task by its ID")
async def delete_task(task_id: int):
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)