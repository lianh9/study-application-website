from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ShareNoteForm(FlaskForm):
    """
    Create form filed 2 string fields for the purpose of sharing notes.
        Parameters:
            FlaskForm : A form parameter from flask_wtf
    """
    share_user_name = StringField('Share With', validators=[DataRequired()])
    note_id = StringField('Note ID', validators=[DataRequired()])
    submit = SubmitField('Share Note')
