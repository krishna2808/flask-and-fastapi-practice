from email.policy import default
import imp
from tkinter.tix import COLUMN
from turtle import title
# from xmlrpc.client import Boolean
from typing import Union

from requests import request
from setuptools import Require
from fastapi import FastAPI , Query
from pydantic import BaseModel, Required

# from sqlalchemy import Column, String, Integer, Boolean
# from  . import schemas

# from . import database as db 


# from database import  * 
app = FastAPI()




class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None



@app.post("/items/")
async def create_item(item: Item):
    return item




@app.get("/itemm/")
async def read_items(q: Union[str, None] = Query(default=Require, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    i =  [ {str(i) : 'this'}   for i in range(60)]
    results = {'items' : i }
    if q:
        results.update({"q": q})
    return results
    
# class User(db.Base):
#     __table_name__ =  "users"
#     id = Column(String, unique=True, index= True)
#     email = Column(String, unique=True, index=True)
#     is_active = Column(Boolean, default=True)
# db.Base.metadata.create_all(bind=db.engine)
    

@app.get('/')
def index():
    return 'hii krishna'


@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}




@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}
# @app.get("/users/me/temp")
# async def read_user_me():
#     return {"user_id": "the current user"}



fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"},{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"},{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "9"},{"item_name": "10"}, {"item_name": "11"}, {"item_name": "12434"}]


@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]



@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}



@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item



# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}




# @app.get("/users")
# async def read_users2():
#     return ["Bean", "Elfo"]

# @app.get("/users")
# async def read_users():
#     return ["Rick", "Morty"]



# @app.get('/items/{user_id}')
# def item_method(user_id: int, user_: schemas.User):
#     print(user_id)
#     return user  




# @app.post('/post_method')
# def post_method():
#     return 'this is post method '
# @app.get('/blog')
# def show():
#     return {'data': 'blog list'}



# @app.get('/blog')
# def create(request :schemas.Blog):

#     return request

# @app.get('/blog/{id}')
# def show(id: int):
#     return {'data':id}




    

