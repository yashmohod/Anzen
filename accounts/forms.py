from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'
    format = ['%d-%m-%Y']

class creatUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['badgeNo','firstName','lastName','dob','collegeId','status','email', 'password1','password2' ]
        widgets = {
            'dob': DateInput(),
        }

class editUserPasword(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1','password2']
