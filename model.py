from pydantic import BaseModel, EmailStr
from typing import List, Any


class SignUpModel(BaseModel):
    email: EmailStr
    password: str
    fullName: str
    userName: str

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class CreateMovie(BaseModel):
    title: str
    description: str
    imageUrl: str
    genre: list
    duration: int
    showtimes: Showtime

class Showtime(BaseModel):
    startTime: str
    price: float
    capacity: int

class Reservation(BaseModel):
    quantity: int