from ipaddress import collapse_addresses
from multiprocessing import synchronize
from random import randint
from statistics import mode
from typing import List
from urllib import response

from hashing import Hash
from requests import session
from sqlalchemy.orm import relationship

# from passlib.context import CryptContext

# from requests import request, session

from fastapi import Depends, FastAPI, HTTPException, status, Response
from sqlalchemy.orm import Session
from schemas import Blogs, ShowBlog, Users, ShowUser, Login

# from . import  models, schemas
# from .database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#database  connection 
# SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:2222@localhost/postgres"

# engine = create_engine( SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine( SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# models file 
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


# from .database import Base



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    email = Column(String)
    password  = Column(String)

    blogs = relationship('Blog', back_populates = 'creator', cascade="all, delete",
        passive_deletes=True,)



class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    
    creator  = relationship("User", back_populates = 'blogs')

Base.metadata.create_all(bind=engine)



app = FastAPI()



def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally :
        db.close     

@app.post('/blog', status_code = status.HTTP_201_CREATED , tags=['Blog'])
def create(request : Blogs, db : Session  = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog', response_model=List[ShowBlog], tags=['Blog'] )
def all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model = ShowBlog, tags=['Blog']) 
def show(id, response: Response, db: Session = Depends(get_db)):

     blog = db.query(Blog).filter(Blog.id == id).first()
     if not blog:
        #  response.status_code = status.HTTP_404_NOT_FOUND
        #  return {'detail': f'blog with id {id} not available '  }
        # same here 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'blog with id {id} not available '  )
     return blog  

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT , tags=['Blog'])
def destory(id, db:Session = Depends(get_db)):
    blog =  db.query(Blog).filter(Blog.id ==id)
    db.commit()
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'blog with id {id} not available '  )
    blog.delete(synchronize_session=False)
    db.commit()
    return 'Done '  

    
@app.put('/blog/{id}', status_code = status.HTTP_202_ACCEPTED , response_model = ShowBlog , tags=['Blog'])
def update(id, request: Blogs, db: Session = Depends(get_db)):
    blog =  db.query(Blog).filter(Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'Blog with id {id} not found ')

    blog.update(request)
    db.commit()
    return 'Update'


# pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')



@app.post('/user' , tags=['User'])
def create_user(request:Users, db: Session = Depends(get_db)):
    
    new_user = User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
@app.get('/user'  , tags=['User'])
def all_user(db: session = Depends(get_db)):
    users = db.query(User).all()
    return users 

@app.get('/user/{id}'  , tags=['User'])
def show_user(id,  db: session = Depends(get_db)):
    
     user = db.query(User).filter(User.id == id).first()
     if not user:
     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'blog with id {id} not available '  )
     return user

@app.post('/login')
def login(request:Login, db: session = Depends(get_db)):
    user = db.query(User).filter(User.name ==request.name )
    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'blog with username not available '  )
    if not Hash.verify(user.password, request.password ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'password has been wrong entered  '  )
        

    return 'yes'





