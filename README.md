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

## License

MIT