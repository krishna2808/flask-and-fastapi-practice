from crypt import methods
import re
from flask import Flask, render_template, request , flash, redirect, url_for, session
# from flask_session import session
from forms import * 



app = Flask(__name__)
app.config['SECRET_KEY'] = 'krishna hu mai'

app.config['UPLOAD_FOLDER'] = 'static/images/'


from modules import *

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
            user = Users.query.filter_by(user_name=form.user_name.data, password=form.password.data).first()
            # for user_data in user:
            if user:  
                if user.is_admin == 'True':
                    return render_template('admin.html')
                elif user.is_admin == 'False':
                    return 'user page '    


                # if(user_data.user_name == form.user_name.data and user_data.password == form.password.data):
                    session["user_name"] = form.user_name.data
                    print('session["user_name"]  : ', session["user_name"] )
                    print("this is ********************", request.form.get('user_name'))
                    form.user_name, form.password = '', '' 
                    print('asfsadfsafasfasf af asf asf as fsa ')
                    return 'yes has been login '
                    return redirect(url_for('dashboard', id=user_data.id))
            message = 'Enter valid username or password '        

    return render_template('login.html', form=form, message=message )                


@app.route("/show_user_data")
def show_user_data(): 

    # user_data = Users.query.all()
    user_data = Users.query.filter_by(is_admin='False')
    if user_data:
      return render_template('show_user_data.html', user_data=user_data, user_available =True)
    return render_template('show_user_data.html', user_available=False)


@app.route('/update_and_delete/<int:id>')
def update_and_delete(id):
    return render_template('delete_and_update_user.html', id=id)


# Update user details 

@app.route("/update/<int:id>", methods = ["POST", "GET"])
def update(id):
     form = Registraion()
     update_user =  Users.query.get_or_404(id)
    #  update_user =  Users.query.filter(id=id)

     if request.method == "POST":
        print("get id  ********* ", update_user)
        update_user.user_name = request.form['user_name']
        update_user.mobile_number = request.form['mobile_number']

        try: 
            db.session.commit()
            print("updaated *****")
            flash("User updated successfully ")
            return 'updated page '
            # return redirect(url_for('show_data'))


        except:
            flash("Error")
            return 'this is error page'
        return 'this page updated'     

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
        return 'data deleted'
    except:
        flash("Error invalid user id ")
        print('Except ****************  ')
    return 'data not deleted'
   
     
@app.route('/add_subject', methods= ['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        if request.form.get('subject_name') != '':
            subject_name = request.form.get('subject_name')
            
