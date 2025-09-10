from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import os
import time
from pydantic import BaseModel
import uvicorn

class Event(BaseModel):
    message: str

app = FastAPI(
    title="DevOps FA",
    description="DevOps FA API",
    version="1.0.0"
)
path = os.path.dirname(os.path.abspath(__file__))
os.makedirs("logs", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>DevOps FA</title>
        </head>
        <body>
            <h1>Welcome to DevOps FA API</h1>
            <p>Use the /docs endpoint to explore the API documentation.</p>
        </body>
    </html>
    """

@app.get("/health", response_class=JSONResponse)
async def health_check():
    return {
        "status": "ok",
        "timestamp": time.time()
    }

@app.post("/log", response_class=JSONResponse)
async def log_event(event: Event):
    try:
        with open(os.path.join(path, "logs/events.log"), "a") as log_file:
            log_file.write(f"{time.time()}: {event.message}\n")
        return {"status": "logged", "timestamp": time.time()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/logs", response_class=JSONResponse)
async def get_logs():
    try:
        with open(os.path.join(path, "logs/events.log"), "r") as log_file:
            logs = log_file.readlines()
        return {"logs": logs}
    except FileNotFoundError:
        return {"logs": []}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/version", response_class=JSONResponse)
async def get_version():
    return {"version": "0.0.1.b"}
    return {"version": "0.0.1.a"}

@app.get("/metrics", response_class=JSONResponse)
async def get_metrics():
    try:
        with open(os.path.join(path, "logs/events.log"), "r") as log_file:
            log_count = len(log_file.readlines())
        return {"event_count": log_count}
    except FileNotFoundError:
        return {"event_count": 0}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/echo/{message}", response_class=JSONResponse)
async def echo_message(message: str):
    return {"message": message}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)