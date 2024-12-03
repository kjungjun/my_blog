from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
import shutil
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts = []

class Post(BaseModel):
    title: str
    content: str
    image_url: str = None

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

@app.post("/upload")
async def create_post(title: str = Form(...), content: str = Form(...), file: UploadFile = File(None)):
    image_url = None
    if file:
        file_location = f"static/images/{file.filename}"
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        image_url = f"/static/images/{file.filename}"
    
    post = Post(title=title, content=content, image_url=image_url)
    posts.append(post)
    return post

@app.delete("/delete/{post_id}")
async def delete_post(post_id: int):
    if post_id >= len(posts) or post_id < 0:
        raise HTTPException(status_code=404, detail="Post not found")
    deleted_post = posts.pop(post_id)
    if deleted_post.image_url:
        image_path = deleted_post.image_url.lstrip("/")
        if os.path.exists(image_path):
            os.remove(image_path)
    return {"message": "Post deleted"}

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(post_id: int, request: Request):
    post = posts[post_id]
    return templates.TemplateResponse("post.html", {"request": request, "post": post})
