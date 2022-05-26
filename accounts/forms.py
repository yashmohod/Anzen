from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from matplotlib import widgets
from . import models
User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'


class TimePickerInput(forms.TimeInput):
        input_type = 'time'

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

class inceidents (forms.Form):
    model = models.inceidents
    fields = ['inceidentName']


class incidentReport (forms.Form):
    model = models.incidentReport
    fields = ['reportedBy','inceident','date','receivedTime','enrouteTime','arivedTime','clearTime','summary']
    widgets = {
        'date': DateInput(),
        'receivedTime' : TimePickerInput(),
        'enrouteTime' : TimePickerInput(),
        'arivedTime' : TimePickerInput(),
        'clearTime': TimePickerInput(),
    }

class muleInspection (forms.Form):
    model = models.muleInspection
    fields = ['reportedBy','date','summary']
    widgets = {
        'date': DateInput(),
    }


class academicLockup (forms.Form):
    model = models.academicLockup
    fields = ['reportedBy','date','startTime','endTime','summary']
    widgets = {
        'date': DateInput(),
        'startTime' : TimePickerInput(),
        'endTime' : TimePickerInput(),
    }

