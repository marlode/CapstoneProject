from tkinter.messagebox import QUESTION
from django.test import TestCase
from ..forms import RegisterForm, SurveyForm, PostForm


class TestModels(TestCase):

    def test_survey_form(self):
        form = SurveyForm(data={
            'QUESTIONONE': 'No Preference',
            'PERSON_CHOICE': '',
            'QUESTIONTWO': 'Positive',
            'QUESTIONTHREE': 0,
            'QUESTIONFOUR': 2010,
            'QUESTIONFIVE': 2,
            'QUESTIONSIX': 'heist'
        })

        self.assertTrue(form.is_valid())

    def test_survey_form_no_data(self):
        form = SurveyForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)