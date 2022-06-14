from flask import Flask, render_template, request , flash, redirect, url_for


from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, validators, PasswordField
from wtforms.validators import DataRequired, EqualTo

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_migrate import Migrate 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'krishna hu mai'
 

# Add Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

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




class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    author =  db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))






# create form class 

class Registraion(FlaskForm):

    user_name = StringField('Username', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number',  validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('confirm_passowrd', message='Passwords must match')])

    submit  = SubmitField('Submit')
    
    def __repr__(self):
        return '<Username %r>' % self.user_name




@app.route('/sign_up', methods = ['GET', 'POST'])

def sign_up():
    form = Registraion()
    print(form)
    success = None 
    if request.method == 'POST': 
       print(' in post ')
       print(form.user_name.data, form.mobile_number.data, form.password.data,  form.submit.data, form.validate_on_submit())
       if form.validate_on_submit():
            user = Users(user_name=form.user_name.data, mobile_number=form.mobile_number.data, password=form.password.data)

            db.session.add(user)
            db.session.commit()
            form.user_name = ''
            print('in validate data ')
            success = "added "
            # return 'Successfully account has been created '

    return render_template('registration.html', form=form, success=success)

# Read data from database of table 

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


# create custom error  pages 

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404 


@app.errorhandler(500)
def page_not_found(error):
    return render_template("errors/500.html")






