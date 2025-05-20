import os
import sys


from fastapi import FastAPI
import uvicorn

# Add main directory to path
MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(MAIN_DIR)

try:
    from logs import log_info
    from api.hello import hello_route
except Exception as e:
    raise ImportError(e) from e

app = FastAPI()

app.include_router(hello_route)

if __name__ == "__main__":
    log_info("Start running the application")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
