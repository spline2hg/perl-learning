from django import forms
from .models import *


class CreateMeetingForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name','description','status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['content']

class AlertsForm(forms.ModelForm):
    class Meta:
        model = Alerts
        fields = ['content']

class Pm_Form(forms.ModelForm):
    class Meta:
        model = PersonalMessage
        fields = ['text','url']


class RequestForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['content']