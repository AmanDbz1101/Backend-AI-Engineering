# AI Rematch Prompt

I used the following prompt to ask an AI to build the same Task API:

---

**Prompt:**

Build a complete CRUD REST API for a to-do list using Python and FastAPI. The API must have the following endpoints:

1. GET / - Returns API info: {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}
2. GET /health - Returns {"status": "ok"}
3. GET /tasks - Returns list of all tasks
4. GET /tasks/{id} - Returns single task by ID, 404 if not found
5. POST /tasks - Creates new task from JSON body {"title": "..."}, returns 201 with created task, validates title is present and non-empty (400 if not)
6. PUT /tasks/{id} - Updates task title and/or done status, returns updated task, 404 if not found, 400 for empty title
7. DELETE /tasks/{id} - Deletes task, returns 204 No Content, 404 if not found

Requirements:
- In-memory storage only (Python list)
- Task object: id (int), title (string), done (boolean)
- Pre-populate with 3 example tasks
- Proper HTTP status codes: 200, 201, 204, 400, 404
- All errors return JSON: {"detail": "error message"}
- Swagger UI documentation at /docs (FastAPI built-in)
- Add endpoint descriptions for Swagger UI
- Single file: main.py
- Run with: python main.py on port 8000

---

This prompt specifies all endpoints, status codes, validation rules, in-memory storage, and Swagger UI requirements.