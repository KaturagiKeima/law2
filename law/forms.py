from django import forms
from .models import User_date, User_question, Question

class ClassTimeForm(forms.ModelForm):

    class Meta:
        model = User_date
        fields = ['sum_question','class_times']
        widgets = {
            'sum_question': forms.NumberInput(attrs={'value':'5','min':'1'}),
            'class_times' : forms.CheckboxSelectMultiple(),
        }

class UserQuestionForm(forms.ModelForm):

    class Meta:
        model = User_question
        fields = ['input_answer']
        widgets = {
            'input_answer' : forms.DateInput()
        }

