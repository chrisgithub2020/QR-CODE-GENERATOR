from fastapi.applications import FastAPI, Request
from fastapi.staticfiles  import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from pydantic import BaseModel
import os

from utils import generate_qr_code

app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), "image")
templates = Jinja2Templates(directory="templates")

class Data(BaseModel):
    url: str


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"image_url":"./images/default.png", "download_name":"default.png"})

@app.post("/generate_code", response_class=HTMLResponse)
def generate_code(link: Data, request: Request):

    file_name = generate_qr_code(link=link.url)
    image_path = Path(f"./images/{file_name}.png")
    if not image_path.is_file():
        return {"error": "No such image"}
    
    return templates.TemplateResponse(request=request, name="replace.html",context={"image_url":f"./images/{file_name}.png", "download_name":file_name})