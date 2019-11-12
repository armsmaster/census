from django import forms
from . import models


class Choice_Form(forms.ModelForm):

    class Meta:
        model = models.Choice
        fields = ('name', 'num_value')


class MapSurveyQuestion_Form(forms.ModelForm):

    class Meta:
        model = models.MapSurveyQuestion
        fields = ('question',)


class MapUserSurvey_Form(forms.ModelForm):

    class Meta:
        model = models.MapUserSurvey
        fields = ('person',)


class MSMC(forms.Form):
    
    def __init__(self, data_choices, *args, **kwargs):
        super(MSMC, self).__init__(*args, **kwargs)
        self.fields['data'].choices = data_choices
    
    data = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)


class SSMC(forms.Form):

    def __init__(self, data_choices, *args, **kwargs):
        super(SSMC, self).__init__(*args, **kwargs)
        self.fields['data'].choices = data_choices
    
    data = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=[])


class NumRange(forms.Form):
    
    data = forms.IntegerField(required=True, widget=forms.HiddenInput)


class Numeric(forms.Form):
    
    data = forms.DecimalField(required=True)


class Txt(forms.Form):
    
    data = forms.CharField(required=True, max_length=2000, widget=forms.Textarea)
