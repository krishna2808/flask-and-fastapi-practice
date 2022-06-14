from email.quoprimime import body_check
from pydantic import BaseModel


class Blogs(BaseModel):
    title : str 
    body : str 

    


# (1)
# class ShowBlog(Blogs):
#     class Config():
#         orm_mode = True
    
# both are same if when extend BaseModel so accoding to our choice you can see 
# (2)

class Users(BaseModel):
    name : str 
    email :str 
    password : str 


class ShowUser(BaseModel):
    name : str 
    email : str 
    class Config():
        orm_model = True 


class ShowBlog(BaseModel):
    title: str 
    id : int 
    body = str 
    creator = ShowUser
    
    class Config():
        orm_mode = True

class Login(BaseModel):
    name : str 
    password : str 
