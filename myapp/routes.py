
from os import error
from re import S
from flask import escape
from sqlalchemy.orm import session
from werkzeug.security import check_password_hash, generate_password_hash
from myapp import myobj
from myapp import db
from myapp.loginforms import LoginForm
from myapp.deleteforms import DeleteForm
from myapp.noteforms import NoteForm
from myapp.searchforms import SearchForm
from myapp.models import User, Notes
from myapp.registerforms import RegisterForm
from flask import render_template, escape, flash, redirect,request
from markdown import markdown
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user



@myobj.route("/")
def home():
    """Return home page 
    """
    return render_template("home.html")

@myobj.route("/home")
def study():
    """
        Return home page (should be in html)
    """
    return render_template("home.html")

@myobj.route("/login", methods=['GET', 'POST'])
def login(): 
    '''
    Get the login in information from the login page and verify if the 
    information matching the exiting User database. If so log user in.
    otherwise, giving user warning message.
        Returns:
            return html pages
    '''
    form = LoginForm()
    # if the user hit submit on the forms page
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        user = User.query.filter_by(email=email).first()
        if user != None:
            passed = check_password_hash(user.password_hash,password)
            if passed == True:
                login_user(user)
                flash("Login Successfully!")
            else: 
                flash("Wrong information, please try again")
        else:
            flash('User doesn not exit, try agian!')
            return redirect('/login')
        return redirect('/home')
    return render_template('login.html',form=form)

@myobj.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    '''
    Logout current user and block user from login required page
        Returns:
            return login html page
    '''
    logout_user()
    flash('Logout Successfully!')
    return redirect('/login')


@myobj.route("/register", methods=['GET', 'POST'])
def register():
    '''
    Get the sign up information from the sign up page and store them
    to the User database. Verify the sign up email if already exit, if
    so, flash message to user that email already exiting, otherwise add
    the new user information to the User database
        Returns:
            return html pages
    '''
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'{form.username.data} registered succesfully')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password_hash']
        password_hash = generate_password_hash(password)
        email = request.form['email']
        if User.query.filter_by(email=email).first():
            flash('Email already exsit')
        add_user = User(username=username,email=email, password_hash=password_hash)
        db.session.add(add_user)
        db.session.commit()
        return redirect('/login')
    return render_template('/register.html', form = form)

@myobj.route('/delete/', methods=['GET', 'POST'])
@login_required
def delete_account():
    '''
    Get the delete information from the delete page and verify if the 
    information matching the exiting User database and if the user are
    in their own account. If so delete the current user from the database.
    otherwise, giving user warning message.
        Returns:
            return html pages
    '''
    form = DeleteForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        user = User.query.filter_by(email=email).first()
        passed = check_password_hash(user.password_hash,password) 
        if user.id == current_user.id and passed == True:   
            try:
                db.session.delete(user)
                db.session.commit()
                flash('Account Deleted Successfully!')
            except:
                flash('Something went wrong, please try agian later')
        else: 
            flash('Wrong Information, Please Try Agian!')
            return redirect('/delete')
    return render_template('/delete.html', form = form)

@myobj.route("/note", methods=['GET', 'POST'])
@login_required
def add_notes():
    '''
    Get the notes information from the add notes page and store notes
    in the Notes database.
        Returns:
            return html pages
    '''
    form = NoteForm()
    if form.validate_on_submit():
        note = Notes(title=form.title.data,user_id = current_user.id,text=form.text.data)
        db.session.add(note)
        db.session.commit()
        flash('Notes added')
    return render_template('note.html',form=form)

@myobj.route("/note_dashboard", methods=['GET', 'POST'])
@login_required
def notes_dashboard():
    '''
    Get current login user's notes information form Notes database
    and display all the notes in the dashboard page and provides
    a search box for user to search their notes by a word
        Returns:
            return html pages
    '''
    form = SearchForm()
    note_id = None
    word = ""
    notes = Notes.query.filter_by(user_id=current_user.id)
    if form.validate_on_submit():
        word = form.search.data
        for i in notes:
            found_test= i.text
            found_title=i.title
            if word in found_test:
                flash('word found in note title : ' +found_title + ', with content : ' + found_test)
        flash('No word found' )
    for note in notes:
        note_id = note.user_id
    return render_template('note_dashboard.html',notes=notes,note_id=note_id,form=form,word=word)
