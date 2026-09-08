from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Deploy to GitHub", "done": False},
]


@app.get("/")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/tasks")
async def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/tasks", status_code=201)
async def create_task(request: Request):
    body = await request.json()
    title = body.get("title")
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    new_task = {"id": new_id, "title": title.strip(), "done": False}
    tasks.append(new_task)
    return new_task


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)