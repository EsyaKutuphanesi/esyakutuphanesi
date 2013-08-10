from flask.ext.wtf import Form, TextField, BooleanField, SelectField, widgets, SelectMultipleField
from flask.ext.wtf import Required

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
    