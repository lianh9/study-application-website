## Code in myapp/routes.py
```python
@myobj.route("/")
def home():
    """
        Return home page 
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


@myobj.route("/share_note", methods=['GET', 'POST'])
@login_required
def share_notes():
    '''
    Get current login user's share notes information from Notes database
    and User database. If the the notes or person user want to share to is
    not exit, provides 404 page with description. If both notes and the person
    the user want to share is in the database, share the notes to the person that
    user entered.
        Returns:
            return html pages
    '''
    form = ShareNoteForm()
    if form.validate_on_submit():
        share_notes_title = str(form.noteSharing.data)
        receiver_email = form.email.data
        receiver_email = str(receiver_email)
        notes = Notes.query.filter_by(title=share_notes_title).first_or_404(description='There is no notes title {} in your account'.format(share_notes_title))
        receiver = User.query.filter_by(email=receiver_email).first_or_404(description='There is no user with {} in the system, please invite the person to sign up account with us'.format(receiver_email))
        receiver_id = receiver.id
        if notes != None and receiver != None:
            for i in notes:
                notes_to_share_title = i.title
                notes_to_share_text = i.text 
                note = Notes(title=notes_to_share_title,user_id = receiver_id,text=notes_to_share_text)
                db.session.add(note)
                db.session.commit()
                flash('Notes shared sucessfully!')
        else : 
            flash('Error, please try agian later')

    return render_template('share_note.html',form=form)

        


@myobj.route("/track",methods = ['GET', 'POST'])
@login_required
def trackhours():
    '''
        Allows the user to input when they worked and how many hours
        they worked. This function will create a list that will store
        the data, so they can track how many hours they worked that day.
            Returns:
                Date
                Integer
    '''
    form = Track()

    if form.validate_on_submit():
        flash(f' data saved')
        hoursworked = form.hours.data
        dateworked = form.datew.data
        organize = Tracker(hours = hoursworked,datew = dateworked)
        db.session.add(organize)
        db.session.commit()
    current = datetime.now().strftime("%m/%d/%Y")
    order = Tracker.query.all()
    return render_template('tracker.html',current = current, form = form, order = order )

@myobj.route("/todo", methods = ['GET', 'POST'])
@login_required
def toDo():
    '''
        Allows the user to create a Todo list that lets them type what is due,
        when it is due, and how important that assignment is (priority)
            Returns:
                String
    '''
    form = ToDo()

    if form.validate_on_submit():
        flash(f' {form.goal.data} added')
        goalname = form.goal.data
        prior = form.prio.data
        dueDate = form.due_date.data
        doList = Todo(goal = goalname, prio = prior,due_date = dueDate)
        db.session.add(doList)
        db.session.commit()
        return redirect ("todo")

    orderList = Todo.query.order_by(Todo.prio).all()
    return render_template('todo.html', form = form, orderList = orderList)
    
@myobj.route("/cards", methods=['GET', 'POST'])
@login_required
def add_card():
    '''
    Stores the card information in the card database.
        Returns:
            return html pages
    '''
    form = FlashCardForm()
    if form.validate_on_submit():
        card = FlashCard(title=form.title.data,user_id = current_user.id,content=form.content.data)
        db.session.add(card)
        db.session.commit()
        flash('Card added')
    return render_template('flashcard.html', form=form)

@myobj.route("/myflashcards", methods=['GET', 'POST'])
@login_required
def my_flashcards():
    '''
    View all the flashcards of the user
        Returns:
            return html pages
    '''
    card_id = None
    cards = FlashCard.query.filter_by(user_id=current_user.id)
    for card in cards:
        card_id = card.user_id
    return render_template('myflashcards.html', cards=cards, card_id=card_id)

@myobj.route("/cardtopdf", methods=['GET', 'POST'])
@login_required
def card_to_pdf():
    '''
    Convert Card to pdf
        Returns:
            return pdf file
    '''
    form = GetFile()
    if form.validate_on_submit():
        name = secure_filename(form.file.data.name)
        form.file.data.save('myapp/static/cards/' +name)
        input_name= 'myapp/static/cards/' +name
        output_name=input_name.split(".html")[0] + ".pdf"
        pdfkit.from_file(input_name, output_name)
        return render_template('cardtopdf.html', form=form, pdf=output_name)
    return render_template('cardtopdf.html', form=form)

```
## Code in myapp/workhrs.py
```python
class Track(FlaskForm):
    '''
        Create form filed for the purpose of tracking hours worked.
                Parameters:
                FlaskForm : A form parameter from flask_wtf
    '''
    hours = IntegerField("How many hours did you work")
    datew = DateField("When did you work(m/d/y)",format = '%m/%d/%Y')
    addH = SubmitField("Save Hours")

```
## Code in myapp/todoforms.py
```python
class ToDo(FlaskForm):
     '''
             Create form filed for the purpose of creating a to do list.
                    Parameters:
                    FlaskForm : A form parameter from flask_wtf
     '''
    goal = StringField(  "What to do            :", validators = [DataRequired()])
    prio = IntegerField("Priority rank", validators = [DataRequired()])
    due_date = DateField("When is it due?(m/d/y):", validators = [DataRequired()], format = '%m/%d/%Y')
    addG = SubmitField("Add to do")
    delG = SubmitField("Remove item")


```
## Code in myapp/deleteforms.py
```python
class DeleteForm(FlaskForm):
    '''
    Create form filed for the purpose of delete account information.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password',validators=[DataRequired()])
    delete = SubmitField('Submit')

```
## code in myapp/loginforms.py
```python
class LoginForm(FlaskForm):
    '''
    Create form filed for the purpose of login account information.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

```
## Code in mapp/models.py
```python

class User(db.Model, UserMixin):
    '''
    Create user database for the purpose of storing user information.
        Parameters:
            db.Model :
            UserMixin: 
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash =db.Column(db.String(128))
    notes = db.relationship('Notes',backref='user',lazy = True)
 #Returns a string as a representation of the object.
    def __repr__(self):
        return f'<{self.username}  {self.email}  {self.password_hash}>'
   
@login_manager.user_loader
def load_user(id):
    '''
    load user's id
        Parameters:
                id     
        Returns:
            int (id) : user id
    '''
    return User.query.get(int(id))

class Notes(db.Model):
    '''
    Create database to store notes information.
        Parameters:
            db.Model 
        Returns:
            return html pages
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    text = db.Column(db.Text)
    date_added = db.Column(db.DateTime,default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)

 #Returns a string as a representation of the object.
    def __repr__(self):
        return f'<{self.title}  {self.text} >'

class Todo(db.Model):
    '''
    Creates a database to store the name and date
    for the todo list
        Parameters:
            db.Model
        Returns:
            String
    '''
    id = db.Column(db.Integer, primary_key = True)
    goal = db.Column(db.String(80))
    prio = db.Column(db.Integer, index = True)
    due_date = db.Column(db.DateTime)

    def __ref(self):
        return f"Todo('{self.goal}', {self.prio})"

class Tracker(db.Model):
    '''
    Creates a database to store the number and date
    to track how many hours they worked
        Parameters:
            db.model
        Returns:
            Date
            integer
    '''
    id = db.Column(db.Integer, primary_key = True)
    hours = db.Column(db.Integer)
    datew = db.Column(db.DateTime)
    
class FlashCard(db.Model):
    '''
    Create database to store flashcard information.
        Parameters:
            db.Model
        Returns:
            return html pages
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.String(128))
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)

 #Returns a string as a representation of the object.
    def __repr__(self):
        return f'<{self.title}  {self.content} {self.date_added}  >'

```
## Code in myapp/noteforms.py
```python
class NoteForm(FlaskForm):
    '''
    Create form filed string and textarea for the purpose of entering notes and the title.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()],widget=TextArea())
    submit = SubmitField('submit')

```
## Code in myapp/registerforms.py
```python

class RegisterForm(FlaskForm):
    '''
    Create form filed for the purpose of signing up account information.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    username = StringField('Username', validators=[DataRequired()])
    password_hash = PasswordField('Password',validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    register = SubmitField('Sign up')

```
## Code in mapp/searchforms.py
```python
class SearchForm(FlaskForm):
    '''
    Create form filed for the purpose of search word in the page.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    '''
    search = StringField('Please enter the word to search notes', validators=[DataRequired()])
    submit = SubmitField('Search')

```
## Code for myapp/init.py
```python
# create Flask class object named myobj
myobj = Flask(__name__,static_url_path="", static_folder="static")
ckeditor =  CKEditor(myobj)
Markdown(myobj, extensions=['fenced_code'],auto_escape=True)
#PageDown(myobj)
# Flask login manager
login_manager = LoginManager()
login_manager.init_app(myobj)
login_manager.login_view = 'login'


myobj.config.from_mapping(
    SECRET_KEY = 'you-will-know',
    # location of sqlite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    
)

db = SQLAlchemy(myobj)
migrate = Migrate(myobj,db)


```
## Code for pomodoro timer
```javascript
//Finding HTML elements by CSS Selectors h2
const setTime = document.querySelector('h2')
//set pomodoro time to 25 min and break time to 5 min
let pomodoro = 1500;
let breakTime = 300;
displayTime(pomodoro);
// Add a click listener to the pomodoro button, once user clicks
// The pomodoro timer will start
const setButton = document.getElementById("start");
setButton.addEventListener("click",function startPomodoro(){
    pomodoroTimer(pomodoro);
});
/**
 * Function to set the time interval for the pomodoro timer
 * and end the pomodoro timer when timer finishes
 * @param {s} second 
 */
function pomodoroTimer(second){
const timer = setInterval (()=>{
    pomodoro--;
    displayTime(pomodoro);
    if(pomodoro <= 0 || pomodoro < 1){
        endTimer();
        breakTimer(breakTime);
        clearInterval(timer);
    }
},1000)
}
/**
 * Function to set the time interval for the break timer
 * and end the break timer when break timer finishes
 * @param {s} second 
 */
function breakTimer(second){
    const timer = setInterval (()=>{
        breakTime--;
        displayTime(breakTime);
        if(breakTime <= 0 || breakTime < 1){
            endBreakTimer();
            clearInterval(timer);
        }
    },1000)
    }
/**
 * Funtion to display time in the format of 00:00
 * and calculate the minites and second  
 * @param {*} second 
 */
function displayTime(second){
    const min = Math.floor(second / 60);
    const sec = Math.floor(second % 60);
    m=format(min);
    s=format(sec)
    setTime.innerHTML = m + ":" + s;
}
/**
 * Function to format the time, when minites or seconds 
 * are less than 10, add 0 in front of them
 * @param {*} temp 
 * @returns temp
 */
function format(temp){
    if (temp < 10){
        temp = '0'+ temp;
    }
    return temp;
}
/**
 * Functions to end the pomodoro timer and display text 
 * Time for break on the website
 */
function endTimer(){
    setTime.innerHTML='Time for break';
}
/**
 * Functions to end the break timer and display text 
 * End for break on the website
 */
function endBreakTimer(){
    setTime.innerHTML='End for break';
}



```

