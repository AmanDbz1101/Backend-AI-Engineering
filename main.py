from fastapi import FastAPI

app = FastAPI(title="Task API", version="1.0")


@app.get("/")
async def root():
    return {"message": "Hello, server!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)