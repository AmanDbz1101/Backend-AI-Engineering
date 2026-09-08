# Task API

A simple CRUD API for managing a to-do list, built with Python and FastAPI. This API allows you to create, read, update, and delete tasks with **PostgreSQL database storage** (data survives container restarts via Docker volume).

## Features

- **Full CRUD operations**: Create, Read, Update, Delete tasks
- **PostgreSQL database storage**: Tasks persist in Postgres (survives server and container restarts)
- **Auto-initialization**: Database and tables created automatically on first run
- **Seed data**: Three example tasks inserted only on first run (no duplicates on restart)
- **Input validation**: Returns `400 Bad Request` for missing or empty titles
- **Proper HTTP status codes**: `200`, `201`, `204`, `400`, `404`
- **Swagger UI**: Interactive API documentation at `/docs`
- **Health check endpoint**: `/health` for monitoring
- **Parameterized queries**: All SQL uses parameterized placeholders for security
- **Docker Compose**: App + database start together with one command
- **Clean architecture**: Repository pattern - storage implementation swapped without changing routes

## Why PostgreSQL in Docker?

- **Production-like**: Uses the same database engine as production
- **Persistent volumes**: Data survives container restarts via Docker named volume
- **Zero configuration**: `docker compose up` starts everything
- **Connection via .env**: Connection string in gitignored `.env`, template in `.env.example`
- **Health checks**: Database health checked before app starts

## Quick Start

### Prerequisites

- Docker and Docker Compose
- (Optional) Python 3.10+ for local development

### Installation & Run with Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd backend-ai-engineering

# Start the entire stack (Postgres + API)
docker compose up -d

# The API will be available at http://localhost:8000
```

### Local Development

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and adjust if needed
cp .env.example .env

# Run the server (requires running Postgres - use `docker compose up -d db`)
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
├── main.py              # FastAPI application (routes only)
├── repository.py        # Postgres repository (storage layer)
├── init.sql             # Database initialization script
├── docker-compose.yml   # Docker Compose for app + db
├── Dockerfile           # App container definition
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Architecture: Repository Pattern

The application uses the **Repository Pattern** to separate the storage layer from the business logic:

- **main.py** - Contains only HTTP routes, no SQL
- **repository.py** - Implements `TaskRepository` with Postgres storage
- **Swappable storage**: Changing from SQLite to Postgres only required replacing `repository.py` - routes unchanged

This proves "switch storage really does change only one file" as intended by the assignment.

## Persistence Verification

Data survives **both** server restarts AND container restarts:

### Test 1: App restart only
```bash
# Create a task
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Test"}'

# Restart only the app container
docker compose restart app

# Verify task still exists
curl http://localhost:8000/tasks
```

### Test 2: Full stack restart (proves Docker volume persistence)
```bash
# Create a task
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Persistence test"}'
# Returns: {"id":5,"title":"Persistence test","done":false}

# Stop and remove everything (containers, network)
docker compose down

# Start everything again
docker compose up -d

# Verify task still exists
curl http://localhost:8000/tasks
# Returns: [{"id":1,"title":"Learn FastAPI","done":false},{"id":2,"title":"Build CRUD API","done":false},{"id":3,"title":"Deploy to GitHub","done":false},{"id":5,"title":"Persistence test","done":false}]
```

**Result**: The "Persistence test" task (id: 5) survives a complete `docker compose down && docker compose up -d` cycle because PostgreSQL data is stored in a Docker named volume (`postgres_data`).

## Database Exploration

The database can be explored directly:

```bash
# Connect to Postgres in the container
docker compose exec db psql -U postgres -d tasks_db

# Or run queries directly
docker compose exec db psql -U postgres -d tasks_db -c "SELECT * FROM tasks;"
```

Example queries:
```sql
-- List all tasks
SELECT * FROM tasks ORDER BY id;

-- Filter completed tasks
SELECT * FROM tasks WHERE done = true;

-- Count tasks
SELECT COUNT(*) FROM tasks;

-- Mark all tasks as done
UPDATE tasks SET done = true;
```

## AI vs Me (Bonus Stage 7 - Week 2)

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

## AI vs Me (Bonus Stage 6 - Week 3)

### Prompt Used

```
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
```

### Differences Found

1. **What the AI did better**: The AI used a context manager for database connections (`with get_db():`) which ensures proper cleanup even on exceptions. It also used `row_factory = sqlite3.Row` for named column access, making the code cleaner than using positional indexes.

2. **What the AI got wrong/missed**: The AI forgot to seed data only when the table is empty - it inserted seed data every time the server started, causing duplicate tasks on each restart. It also used `AUTOINCREMENT` which is unnecessary in SQLite (regular `INTEGER PRIMARY KEY` is sufficient and faster). The AI's UPDATE query didn't handle partial updates correctly - it would overwrite fields with NULL when only one field was provided.

3. **What my prompt forgot to specify**: I didn't explicitly mention "seed only when empty" clearly enough, nor did I specify the exact UPDATE logic for partial updates (only update fields that are provided). The AI silently decided to use AUTOINCREMENT and INSERT on every startup.

## License

MIT