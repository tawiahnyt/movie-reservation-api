

from fastapi import FastAPI, Depends
from typing import Any
from fastapi.responses import JSONResponse
from auth import get_current_user, create_token
from prisma import Prisma
from model import SignUpModel, LoginModel, CreateBlogModel
from utils import check_password_strenth, get_password_hash, verify_password


app = FastAPI()
prisma = Prisma()

@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.post("/sign-up")
async def signUp(data: SignUpModel):
    existing_user = await prisma.user.find_unique(where={'email': data.email})
    if existing_user:
        return JSONResponse(status_code=400,content={'error': 'User email already exists'})

    existing_userName = await prisma.user.find_unique(where={'userName': data.userName})
    if existing_userName:
        return JSONResponse(status_code=400,content={'error': 'Username already exists'})

    check_password_strenth(data.password)

    hashed_password = get_password_hash(data.password)

    user = await prisma.user.create(
        data = {
            "fullName": data.fullName,
            "userName": data.userName,
            "email": data.email,
            "password": hashed_password
        }
    )
    return {
        "message": "User created successfully",
        "access_token": create_token(fullName=user.fullName, email=user.email, username=user.userName, userId=user.id),
        "token_type": "bearer"
        }


@app.post("/login")
async def login(data: LoginModel):
    existing_user = await prisma.user.find_unique(where={'email': data.email})
    if not existing_user:
        return JSONResponse(status_code=400,content={'error': 'User not found'})

    check_password = verify_password(data.password, existing_user.password)
    if not check_password:
        return JSONResponse(status_code=400,content={'error': 'invalid username or password'})

    return {
        "message": "User created successfully",
        "access_token": create_token(fullName=existing_user.fullName, email=existing_user.email, username=existing_user.userName, userId=existing_user.id),
        "token_type": "bearer"
        }



@app.post("/post-blog")
async def createBlogPost(data: CreateBlogModel, user: Any = Depends(get_current_user)):
    print(user)
    blog = await prisma.blog.create(
        data={
            "title": data.title,
            "category": data.category,
            "content": data.content,
            "tags": data.tags,
            "userId": user["userId"]
        }
    )
    return {
        "message": "Blog post created successfully",
        "data": blog
            }


@app.get("/blogs")
async def getBlogPost(user: Any = Depends(get_current_user)):
    blogs = await prisma.blog.find_many(
        where=({"userId": user["userId"]})
    )
    return {
        "message": "Blog post fetched successfully",
        "data": blogs
            }