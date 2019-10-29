from django import forms
from . import models


class Choice_Form(forms.ModelForm):

    class Meta:
        model = models.Choice
        fields = ('name',)


class MapSurveyQuestion_Form(forms.ModelForm):

    class Meta:
        model = models.MapSurveyQuestion
        fields = ('question',)


class MapUserSurvey_Form(forms.ModelForm):

    class Meta:
        model = models.MapUserSurvey
        fields = ('person',)


class MSMC(forms.Form):
    data = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)


class SSMC(forms.Form):
    data = forms.ChoiceField(required=True, widget=forms.RadioSelect)
