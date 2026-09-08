from fastapi import FastAPI, HTTPException, Request, Response
from repository import TaskRepository

app = FastAPI(title="Task API", version="1.0")

# Repository instance - swap storage implementation here
repo = TaskRepository()


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
    return repo.get_all()


@app.get("/tasks/{task_id}", summary="Get a task by ID", description="Returns a single task by its ID")
async def get_task(task_id: int):
    task = repo.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201, summary="Create a new task", description="Creates a new task with the given title")
async def create_task(request: Request):
    body = await request.json()
    title = body.get("title")
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="Title is required")
    
    return repo.create(title)


@app.put("/tasks/{task_id}", summary="Update a task", description="Updates a task's title and/or done status")
async def update_task(task_id: int, request: Request):
    body = await request.json()
    title = body.get("title")
    done = body.get("done")
    
    if title is not None and (not title or not title.strip()):
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    try:
        task = repo.update(task_id, title=title, done=done)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task", description="Deletes a task by its ID")
async def delete_task(task_id: int):
    deleted = repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)