from flask import Flask, render_template, request , flash, redirect, url_for, session
# from flask_session import session
from forms import * 
# from werkzeug  import secure_filename

from werkzeug.utils import secure_filename
import uuid as uuid

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'krishna hu mai'


from modules import *

app.config['UPLOAD_FOLDER'] = 'static/images/'


@app.route('/show_post/<int:id>')
def show_post(id):
      posts = Post.query.filter_by(author=id)     
      user_data = Users.query.get(id)
      for i in  posts:
        print("post details : ",  i.post_pic, i.content)
      return render_template('show_post.html', posts=posts, user_name=user_data.user_name)


@app.route('/profile/<int:id>', methods=['POST',  'GET'])
def profile(id):
    try:
        print("in try block ")
        user_detail = Users.query.get(id)
         
        if request.method == 'POST':
          
            user_name = request.form.get('user_name')
            
            mobile_number = request.form.get('mobile_number')

            about_author = request.form.get('about_author')
            file = request.files['user_pic']

            filename = secure_filename(file.filename)
            if filename != '':
                filename = str(uuid.uuid1()) +  filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user_detail.user_name = user_name
                user_detail.mobile_number = mobile_number
                user_detail.about_author = about_author
                user_detail.user_pic =  filename
                db.session.commit()
                flash("Your details uploded successfully ")
            return redirect(url_for('profile', id=id))
            
    except:
          return redirect(url_for('log_in'))

    return render_tem


class Posts(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()] )
    post_pic = FileField('Post Pic', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit  = SubmitField('Submit',  validators=[DataRequired()])plate('profile.html', user_detail = user_detail)




@app.route('/delete_post/<int:id>')
def delete_post(id):
    post_delete = Post.query.get_or_404(id)
    print('User delete *********** : ', post_delete)
    try:
        db.session.delete(post_delete)
        db.session.commit()
    except:
      flash("Error invalid user id ")
      return 'deleted post'
    finally:
        return  'deleted'





@app.route('/add_post/<int:id>', methods= ['POST', 'GET'])
def add_post(id):
    form = Posts()
    user_detail =  Users.query.get(id)

    if request.method == 'POST':
       print('in post ************* ')
       if form.validate_on_submit():
           
           file = request.files['post_pic']
           print("in validate_on_submit *************  ")

           filename = secure_filename(file.filename)
           filename = str(uuid.uuid1()) +  filename
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

           post =  Post(title=form.title.data, content=form.content.data, author=id, post_pic=filename )
           db.session.add(post)
           db.session.commit()
           flash("successfully add post")
           return redirect(url_for('dashboard', id=id))
       else:
           flash("Enter field ")
           form.title.data, form.content.data = '', ''

    return render_template('add_post.html', form=form, user_detail=user_detail)       


@app.route('/dashboard/<int:id>')
def dashboard(id):
    # get_or_404 if id is not available so error occure and program break and get() is not error occuring.
    print('session["user_name"]  ', session["user_name"], session.get("user_name") )

    if session.get("user_name"):
        user_detail =  Users.query.get(id)
        all_post = Post.query.order_by(Post.date_posted.desc())
        user_obj = Users()


        return render_template('dashboard.html', user_detail=user_detail, id=id, all_post=all_post, user_obj=user_obj)
    return redirect(url_for('log_in'))    




@app.route('/sign_up', methods = ['GET', 'POST'])

def sign_up():
    form = Registraion()
    print(form)
    success = None 
    if request.method == 'POST': 
       print(' in post ')
       print(form.user_name.data, form.mobile_number.data, form.password.data,  form.submit.data, form.validate_on_submit())
       if form.validate_on_submit():
            user = Users.query.filter_by(user_name=form.user_name.data, password=form.password.data).first()
            if(user == None):
                user = Users(user_name=form.user_name.data, mobile_number=form.mobile_number.data, password=form.password.data)


                db.session.add(user)
                db.session.commit()

                print('in validate data ')
                success = "added "
                return redirect(url_for('log_in'))
            else:
                success = 'User Name is already exist'

                   
                # return 'Successfully account has been created '
       # return redirect(url_for('sign_up'))        
       form.user_name.data  = ''
       form.password.data = ''
       form.mobile_number.data = ''    
       form.submit.data = ''

    return render_template('registration.html', form=form, success=success)

# Read data from database of table 


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    message = None 
    form = Login()
    if request.method == 'POST':
        print(form.user_name.data, form.password.data)
        if form.validate_on_submit():
            user = Users.query.filter_by(user_name=form.user_name.data, password=form.password.data)
            for user_data in user:
                if(user_data.user_name == form.user_name.data and user_data.password == form.password.data):
                    session["user_name"] = form.user_name.data
                    print('session["user_name"]  : ', session["user_name"] )
                    print("this is ********************", request.form.get('user_name'))
                    form.user_name, form.password = '', '' 
                    print('asfsadfsafasfasf af asf asf as fsa ')
                    return redirect(url_for('dashboard', id=user_data.id))
            message = 'Enter valid username or password '        

    return render_template('login.html', form=form, message=message )                



@app.route('/log_out/<int:id>')
def log_out(id):
    session["user_name"] = None 
    return redirect(url_for('log_in'))


@app.route("/show_data")
def show_data(): 
    user_data = Users.query.order_by(Users.date_added)
    return render_template('show_data.html', user_data=user_data)

@app.route('/update_and_delete/<int:id>')
def update_and_delete(id):
    return render_template('delete_and_update_user.html', id=id)


# Update user details 

@app.route("/update/<int:id>", methods = ["POST", "GET"])
def update(id):
     form = Registraion()
     update_user =  Users.query.get_or_404(id)
     if request.method == "POST":
        print("get id  ********* ", update_user)
        update_user.user_name = request.form['user_name']
        update_user.mobile_number = request.form['mobile_number']

        try: 
            db.session.commit()
            print("updaated *****")
            flash("User updated successfully ")
            return redirect(url_for('show_data'))


        except:
            flash("Error")
            return 'this is error page'

     return render_template('update_data.html', form=form, update_user=update_user )


@app.route('/delete/<int:id>')
def delete(id):
    print('id *********** : ', id)
    user_delete = Users.query.get_or_404(id)
    print('User delete *********** : ', user_delete)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        print('User delete ***************************  ')
        flash("user deleted ")
    except:
      flash("Error invalid user id ")
      print('Except ****************  ')
    finally:
        return  redirect(url_for('show_data'))



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/username/<name>')
def username(name):
    return f"my name fd is this {name}"







