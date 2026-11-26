from pathlib import Path
import traceback
import uvicorn

from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from backend import f_run_travel_agent

BASE_DIR = Path(__file__).resolve.parent

app = FastAPI(
    title="Jajabor AI - Intelligence Meets Exploration",
    description="Langgraph Multi-Agent Travel Planner with Fast API frontend",
    version="1.0.0"
)

## Mount static folder
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

# mount template folder
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)