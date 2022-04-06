from cProfile import label
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
    CHOICES =       (('Director','Director'),
                    ('Actor','Actor'),
                    ('No Preference','No Preference'),)
    CHOICESTWO =    (('Sad','Sad'),
                    ('Happy','Happy'),
                    ('Neutral','Neutral'),)
    CHOICESTHREE =  ((0,'Action'),
                    (1,'Adventure'),
                    (2,'Animation'),
                    (3,'Comedy'),
                    (4,'Crime'),
                    (5,'Documentary'),
                    (6,'Drama'),
                    (7,'Family'),
                    (8,'Fantasy'),
                    (9,'History'),
                    (10,'Horror'),
                    (11,'Music'),
                    (12,'Mystery'),
                    (13,'Romance'),
                    (14,'Science Fiction'),
                    (15,'TV Movie'),
                    (16,'Thriller'),
                    (17,'War'),
                    (18,'Western'),)
    CHOICESFOUR =   ((2020,'2020s'),
                    (2010,'2010s'),
                    (2000,'2000s'),
                    (1990,'1990s'),
                    (1980,'1980s'),
                    (1970,'1970s'),
                    (1960,'1960s'),)
    CHOICESFIVE =   ((0,'1 Star'),
                    (2,'2 Stars'),
                    (4,'3 Stars'),
                    (6,'4 Stars'),
                    (8,'5 Stars'),)

    CHOICESSIX =   (('Heist','Heist'),
                    ('Space','Space'),
                    ('True Story','True Story'),
                    ('Sports','Sports'),
                    ('No Preference','No Preference'),)
    QUESTIONONE     = forms.ChoiceField(label="Choose Preferred Director, Actor, or No Preference:",choices=CHOICES, widget=forms.RadioSelect())  
    PERSON_CHOICE   = forms.CharField(label="Name of Actor/Director, ex: Tom Hanks (leave empty if No Preference):", required=False)
    QUESTIONTWO     = forms.ChoiceField(label="Choose Movie Mood:",choices=CHOICESTWO, widget=forms.RadioSelect())  
    QUESTIONTHREE   = forms.ChoiceField(label="Choose Preferred Movie Genres:",choices=CHOICESTHREE, widget=forms.RadioSelect())
    QUESTIONFOUR    = forms.ChoiceField(label="Choose Preferred Decade:",choices=CHOICESFOUR, widget=forms.RadioSelect())  
    QUESTIONFIVE    = forms.ChoiceField(label="Choose Preferred Rating:",choices=CHOICESFIVE, widget=forms.RadioSelect())
    QUESTIONSIX     = forms.ChoiceField(label="Choose Preferred Settings:",choices=CHOICESSIX, widget=forms.RadioSelect())
    
    

    