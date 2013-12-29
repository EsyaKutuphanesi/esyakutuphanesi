from flask_security.forms import RegisterForm
from flask_wtf import Form, TextField,Required

class ExtendedRegisterForm(RegisterForm):
    name = TextField('Ad Soyad', [Required()])
    nickname = TextField('Takma Ad', [Required()])