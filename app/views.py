"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from ast import Str
from .forms import ContactForm, LoginForm, SignupForm
from app import app, login_manager
from app import mail
from app.forms import LoginForm, SignupForm, ContactForm, TelemetryForm, SleepmodeForm, StationmodeForm, UpdateForm
from app.models import UserProfile, FindUser
from flask_mail import Message
from flask import render_template, request, redirect, url_for, flash,  session, abort, send_from_directory,  abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename 
from werkzeug.security import check_password_hash
 

###
# Routing for your application.
###

@app.route('/login/', methods=['POST', 'GET'])
def login(): 

    form = LoginForm()

    if request.method == 'GET':
        return render_template("login.html", form=form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserProfile(request.form.get('username'),request.form.get('email'),request.form.get('password'))
            state = user.login() 
            if not state:
                flash("Invalid username or password","danger")
                return render_template( "login.html", form=form)
            else: 
                # get user id, load into session 
                login_user(user, remember=True) 
                next = request.args.get('next')
                   
                flash('You were logged in', 'success')
                return redirect(next or url_for('home'))
        else:
            flash_errors(form)
            return render_template("login.html", form=form)




@app.route('/signup/', methods=["GET","POST"])
def signup():
    """Render website's signup page."""
    
    form = SignupForm()

    if request.method == "GET":
        return render_template('signup.html', form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            user = UserProfile(request.form.get('username'),request.form.get('email'),request.form.get('password'))
            state = user.signup()
            if state == "Account already exist":
                flash('Account already exist', 'danger')
                return redirect( url_for('signup'))
            if state == "Account created":
                flash('Account created', 'success')
                return redirect( url_for('home'))
        else:
            flash_errors(form)
            return render_template("signup.html", form=form)
            

        


@app.route("/logout/")
def logout(): 
    logout_user() 
    flash('Logged out successfully.', 'danger')
    return redirect(url_for("home"))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    one = FindUser().find(id) 
    if not one == None:
        user = UserProfile(one['username'],one['email'],one['password'])
        return user 
    return None



@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')



@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/dashboard/')
@login_required
def dashboard():
    """Render the website's about page."""
    return render_template('dashboard.html')


@app.route('/contact/',methods=['POST','GET'])
def contact():
    form = ContactForm()

    if request.method == 'GET':
        return render_template('contact.html',form=form)
        

    if request.method == "POST":    
        if form.validate_on_submit():
            subject = request.form['subject']
            name    = request.form['name']
            email   = request.form['email']
            message = request.form['message']
                   
            msg = Message(subject, sender=(name,"from@example.com "),recipients=[email])
            msg.body = message
            mail.send(msg)
            flash('Your e-mail was successfully sent!','success')
            return redirect(url_for('home')) 
        else:
            flash_errors(form)    
            return render_template('contact.html',form=form)

        
@app.route('/control/',methods=['GET'])
def control():
    form            = TelemetryForm()
    sleepmode       = SleepmodeForm()
    stationmode     = StationmodeForm()
    update          = UpdateForm()
    if request.method == 'GET':
        return render_template('control.html', form = form, sleepmode = sleepmode, stationmode = stationmode, update = update)
    return redirect(url_for('page_not_found'))



###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
