from backend.core.asgi import app
import uvicorn
import sys

if __name__ == "__main__":
    uvicorn.run(app)