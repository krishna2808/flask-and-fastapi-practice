
from blog import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate 


# Add Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 

#initialize the database 
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    mobile_number = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String(20), nullable=True)
    user_pic = db.Column(db.String(255), nullable=True)
    about_author  = db.Column(db.String(200), nullable=True)
    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    post_pic = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text)
  
    author =  db.Column(db.Integer , db.ForeignKey('users.id', ondelete="cascade"))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    # slug = db.Column(db.String(255))


    # children = relationship("Post", cascade="all,delete", backref="Users")
