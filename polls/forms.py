from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class Choice_Form(forms.ModelForm):

    class Meta:
        model = models.Choice
        fields = ('name', 'num_value')
        labels = {
            'name':         'Текстовое значение',
            'num_value':    'Численное значение',
        }


class ChoiceList(forms.ModelForm):

    class Meta:
        model = models.ChoiceList
        fields = ('name',)
        labels = {
            'name':         'Название',
        }


class QGroup(forms.ModelForm):
    
    class Meta:
        model = models.QuestionGroup
        fields = ('name', 'parent')
        labels = {
            'name':         'Название группы',
            'parent':       'Входит в группу',
        }


class Question(forms.ModelForm):

    class Meta:
        model = models.Question
        fields = ('group', 'name', 'text', 'data_type',)
        labels = {
            'name':         'Название вопроса',
            'text':         'Текст вопроса',
            'data_type':    'Тип вопроса',
            'group':        'Группа'
        }


class Question_ChoiceList(forms.ModelForm):

    class Meta:
        model = models.Question
        fields = ('choice_list',)
        labels = {
            'choice_list':  'Список вариантов ответа',
        }


class Question_Range(forms.ModelForm):

    class Meta:
        model = models.Question
        fields = ('range_min', 'range_max', 'range_step',)
        labels = {
            'range_min':    'Нижняя граница диапазона',
            'range_max':    'Верхняя граница диапазона',
            'range_step':   'Шаг',
        }


class MapSurveyQuestion_Form(forms.ModelForm):

    class Meta:
        model = models.MapSurveyQuestion
        fields = ('question',)
        labels = {
            'question': 'Вопрос',
        }


class MapSurveyQuestion_Condition_Form(forms.ModelForm):

    class Meta:
        model = models.MapSurveyQuestion
        fields = ('condition_question', 'condition_answer',)
        labels = {
            'condition_question': 'Связанный вопрос',
            'condition_answer': 'Ответ, являющийся условием',
        }


class MapSurveyQuestion_Mandatory_Form(forms.ModelForm):

    class Meta:
        model = models.MapSurveyQuestion
        fields = ('is_mandatory',)
        labels = {
            'is_mandatory': 'Вопрос обязательный?',
        }


class MapUserSurvey_Form(forms.ModelForm):

    class Meta:
        model = models.MapUserSurvey
        fields = ('person',)
        labels = {
            'person': 'Респондент',
        }


class MSMC(forms.Form):
    
    def __init__(self, data_choices, *args, **kwargs):
        super(MSMC, self).__init__(*args, **kwargs)
        self.fields['data'].choices = data_choices
    
    data = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)


class SSMC(forms.Form):

    def __init__(self, data_choices, *args, **kwargs):
        super(SSMC, self).__init__(*args, **kwargs)
        self.fields['data'].choices = data_choices
    
    data = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=[])


class NumRange(forms.Form):
    
    data = forms.IntegerField(required=False, widget=forms.HiddenInput)


class Numeric(forms.Form):
    
    data = forms.DecimalField(required=False)


class Txt(forms.Form):
    
    data = forms.CharField(required=False, max_length=2000, widget=forms.Textarea)


class Person(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ('email', 'name_first', 'name_second', 'name_last', 'birth_date', 'sex', 'title')
        labels = {
            'email':        'Email', 
            'name_first':   'Имя', 
            'name_second':  'Отчество', 
            'name_last':    'Фамилия', 
            'birth_date':   'Дата рождения', 
            'sex':          'Пол', 
            'title':        'Должность'
        }
        widgets = {
            'birth_date':   DateInput(),
        }


class Survey(forms.ModelForm):
    class Meta:
        model = models.Survey
        fields = ('name', 'description', 'create_date')
        labels = {
            'name':         'Название опроса', 
            'description':  'Приветствие',
            'create_date':  'Дата создания',
        }
        widgets = {
            'create_date':   DateInput(),
        }

