from flask.ext.wtf import Form, TextField, BooleanField, SelectField, widgets, SelectMultipleField, PasswordField
from flask.ext.wtf import Required,validators
from models import User

class SearchForm(Form):
    context_list = [('category','Category'),
                    ('thing','Thing'),
                    ('user','User')]
    search_key = TextField('search_key', validators = [Required()])
    context = SelectField('context', choices=context_list )
    
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    
class CategoryForm(Form):
    category_list = None
    def __init__(self,_category_list):
        self.category_list= _category_list
        categories = [(x.id, x.id) for x in self.category_list]
        self.checkboxes =  MultiCheckboxField('Label', choices=categories)
        
class RegistrationForm(Form):
    name = TextField('Name', [
        validators.Length(min=4, max=25),
        validators.Required()
    ])
    nickname = TextField('Nickname', [
        validators.Length(min=4, max=25),
        validators.Required()
    ])
    email = TextField('Email Address', [
        validators.Length(min=6, max=35),
        validators.Required()
    ])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])
    
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data).first()
        if user:
            self.email.errors.append('There is already a user registered with this email')
            return False
        
        user = User.query.filter_by(
            nickname=self.nickname.data).first()
        if user:
            self.nickname.errors.append('This nickname is already taken')
            return False
        
        return True
    