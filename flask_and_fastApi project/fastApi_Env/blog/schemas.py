from optparse import Option
from typing import Optional
from pydantic import BaseModel 



class Blog(BaseModel):
    title : str 
    body : str 
class User(BaseModel):
    name : str
    password : str
    address : Optional[str]=None

        
