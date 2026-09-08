from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Deploy to GitHub", "done": False},
]


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
    return tasks


@app.get("/tasks/{task_id}", summary="Get a task by ID", description="Returns a single task by its ID")
async def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/tasks", status_code=201, summary="Create a new task", description="Creates a new task with the given title")
async def create_task(request: Request):
    body = await request.json()
    title = body.get("title")
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    
    new_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    new_task = {"id": new_id, "title": title.strip(), "done": False}
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", summary="Update a task", description="Updates a task's title and/or done status")
async def update_task(task_id: int, request: Request):
    body = await request.json()
    title = body.get("title")
    done = body.get("done")
    
    if title is not None and (not title or not title.strip()):
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            if title is not None:
                tasks[i]["title"] = title.strip()
            if done is not None:
                tasks[i]["done"] = bool(done)
            return tasks[i]
    
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task", description="Deletes a task by its ID")
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)