from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import PlainTextResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime
import base64

app = FastAPI()

posts_memory = []

# Question1
@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return PlainTextResponse(content="pong", status_code=200)

# --------------
def check_basic_auth(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    encoded_credentials = auth_header.split(" ")[1]
    decoded_bytes = base64.b64decode(encoded_credentials)
    decoded_credentials = decoded_bytes.decode("utf-8")

    username, password = decoded_credentials.split(":")
    if username != "admin" or password != "123456":
        raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/ping/auth", response_class=PlainTextResponse)
def ping_auth(request: Request = Depends(check_basic_auth)):
    return PlainTextResponse(content="pong", status_code=200)

# Question 2
@app.get("/home", response_class=HTMLResponse)
def home():
    return HTMLResponse(content="<h1>Welcome home!</h1>", status_code=200)

# Question 3
@app.exception_handler(404)
def not_found_handler(request: Request, exc):
    return HTMLResponse(content="<h1>404 NOT FOUND</h1>", status_code=404)

# Question 4 5 6
class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime

@app.post("/posts", response_model=List[Post], status_code=201)
def create_posts(new_posts: List[Post]):
    posts_memory.extend(new_posts)
    return posts_memory

@app.get("/posts", response_model=List[Post])
def get_posts():
    return posts_memory
