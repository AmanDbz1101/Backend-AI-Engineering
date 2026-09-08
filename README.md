# Task API

A simple CRUD API for managing a to-do list, built with Python and FastAPI. This API allows you to create, read, update, and delete tasks with in-memory storage.

## Features

- **Full CRUD operations**: Create, Read, Update, Delete tasks
- **In-memory storage**: Tasks are stored in a Python list (data persists only while server runs)
- **Input validation**: Returns `400 Bad Request` for missing or empty titles
- **Proper HTTP status codes**: `200`, `201`, `204`, `400`, `404`
- **Swagger UI**: Interactive API documentation at `/docs`
- **Health check endpoint**: `/health` for monitoring

## Quick Start

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)

### Installation & Run

```bash
# Clone the repository
git clone <your-repo-url>
cd backend-ai-engineering

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get a single task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Example Usage

### Create a task
```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy milk"}'
```

**Response:**
```
HTTP/1.1 201 Created
date: Tue, 08 Sep 2026 11:07:42 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

### List all tasks
```bash
curl -i http://localhost:8000/tasks
```

### Get a single task
```bash
curl -i http://localhost:8000/tasks/1
```

### Update a task
```bash
curl -i -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated task", "done": true}'
```

### Delete a task
```bash
curl -i -X DELETE http://localhost:8000/tasks/1
```

## Swagger UI

Interactive API documentation is available at **http://localhost:8000/docs**

![Swagger UI](docs/swagger.png)

*Open http://localhost:8000/docs in your browser to explore and test all endpoints interactively.*

## Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Missing or empty title |
| 404 | Not Found - Task with given ID doesn't exist |
| 422 | Validation Error - Invalid request format |

All errors return JSON:
```json
{"detail": "Error message"}
```

## Project Structure

```
.
├── main.py           # FastAPI application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## AI vs Me (Bonus Stage 7)

### Prompt Used

```
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
```

### Differences Found

1. **What the AI did better**: The AI used Pydantic models (`TaskCreate`, `TaskUpdate`) for request validation, which provides automatic request parsing, type coercion, and OpenAPI schema generation. This is more idiomatic FastAPI and reduces boilerplate. The AI also used `next()` with generator expressions for cleaner task lookup instead of manual loops.

2. **What the AI got wrong/missed**: The AI's version returns **422 Unprocessable Entity** for missing `title` field (FastAPI's default Pydantic validation error) instead of the required **400 Bad Request**. My manual validation approach correctly returns 400 for both missing and empty titles. The AI also omitted the `description` field in endpoint decorators, so Swagger UI shows less documentation. The AI used `global tasks` in DELETE which is less clean than `list.pop()`.

3. **What my prompt forgot to specify**: I didn't explicitly require that missing fields return 400 (not 422), nor did I specify that endpoint descriptions should be included for richer Swagger UI. The AI silently chose Pydantic models and FastAPI's default validation behavior, which differs from the assignment's explicit 400 requirement.

### Second Rematch

After improving the prompt to explicitly require "return 400 Bad Request (not 422) for missing or empty title" and "include description in each endpoint for Swagger UI", the AI generated code much closer to my hand-built version, using manual validation instead of Pydantic models and adding full endpoint descriptions.

## License

MIT