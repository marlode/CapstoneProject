from tkinter.messagebox import QUESTION
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

from crispy_forms.helper import *
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]


class SurveyForm(forms.Form):
    CHOICES =       (('a','Horror'),
                    ('b','Action'),
                    ('c','Romance'),
                    ('d','Comedy'),)
    CHOICESTWO =    (('a','Sad'),
                    ('b','Happy'),
                    ('c','Angry'),
                    ('d','Lazy'),)
    CHOICESTHREE =  (('a','Magic'),
                    ('b','Computers'),
                    ('c','Music'),
                    ('d','Cats'),)
    CHOICESFOUR =   (('a','Matters'),
                    ('b','Doesn\'t Matter'))
    CHOICESFIVE =   (('a','1 Star'),
                    ('b','2 Stars'),
                    ('c','3 Stars'),
                    ('d','4 Stars'),
                    ('e','5 Stars'),)
    QUESTIONONE     = forms.MultipleChoiceField(label="Movie Genre:",choices=CHOICES, widget=forms.CheckboxSelectMultiple())  
    QUESTIONTWO     = forms.MultipleChoiceField(label="Mood Today:",choices=CHOICESTWO, widget=forms.CheckboxSelectMultiple())  
    QUESTIONTHREE   = forms.MultipleChoiceField(label="Topic:",choices=CHOICESTHREE, widget=forms.CheckboxSelectMultiple())
    QUESTIONFOUR    = forms.MultipleChoiceField(label="Cast:",choices=CHOICESFOUR, widget=forms.CheckboxSelectMultiple())  
    QUESTIONFIVE    = forms.MultipleChoiceField(label="Review Ratings:",choices=CHOICESFIVE, widget=forms.CheckboxSelectMultiple())

    