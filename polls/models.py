from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import datetime
import random


class Survey(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    create_date = models.DateField(default=datetime.date.today, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def answers(self):
        return Answer.objects.filter(survey_instance__survey=self)
        
    def errors(self):
        output = []
        questions = []
        questions_with_cond = []
        for msq in self.questions.all():
            q = msq.question
            q_string = '<{}>'.format(q)
            if msq.condition_question:
                q_string += '. Condition Question: <{cq}> (Answer: <{ca}>)'.format(cq=msq.condition_question, ca=msq.condition_answer)
                if q_string not in questions_with_cond:
                    questions_with_cond.append(q_string)
                else:
                    err = 'Duplicate Question <b>{}</b>'.format(q_string)
                    if err not in output:
                        output.append(err)
                if '<{}>'.format(q) in questions:
                    err = 'Duplicate Question <b>{}</b>'.format(q)
                    if err not in output:
                        output.append(err)
            else:
                if q_string not in questions:
                    questions.append(q_string)
                else:
                    err = 'Duplicate Question <b>{}</b>'.format(q_string)
                    if err not in output:
                        output.append(err)
                if sum([1 for x in questions_with_cond if q_string in x]) > 0:
                    err = 'Duplicate Question <b>{}</b>'.format(q_string)
                    if err not in output:
                        output.append(err)
        persons = []
        for msp in self.persons.all():
            p = msp.person
            if p not in persons:
                persons.append(p)
            else:
                err = 'Duplicate Assignment <b>{}</b>'.format(p)
                if err not in output:
                    output.append(err)
        return output
            

class ChoiceList(models.Model):
    name = models.CharField(max_length=200)
    
    def has_undef_numeric_values(self):
        for choice in self.choices.all():
            if choice.num_value is None:
                return True
        return False
    
    def __str__(self):
        return self.name


class Choice(models.Model):
    choice_list = models.ForeignKey(ChoiceList, on_delete=models.CASCADE, related_name='choices')
    name = models.CharField(max_length=500)
    num_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return 'Choice <{n}> (Choice List <{l}>)'.format(l=self.choice_list.name, n=self.name)


class QuestionGroup(models.Model):
    name = models.CharField(max_length=500)
    parent = models.ForeignKey('QuestionGroup', on_delete=models.CASCADE, blank=True, null=True, related_name='subgroups')
    
    def level(self):
        if not self.parent:
            return 1
        else:
            return self.parent.level() + 1
    
    def path(self):
        if not self.parent:
            return self.name
        return '{p} / {s}'.format(p=self.parent.path(), s=self.name)
    
    def __str__(self):
        return self.path()
        
    def all_questions(self):
        output = []
        for x in self.questions.all():
            output.append(x)
        for sg in self.subgroups.all():
            sgq = sg.all_questions()
            for x in sgq:
                output.append(x)
        return output
        
    def all_questions_count(self):
        aq = self.all_questions()
        return len(aq)


class Question(models.Model):

    TEXT = 'TEXT'
    NUMBER = 'NUMBER'
    NUMBER_RANGE = 'NUMBER_RANGE'
    MSMC = 'MSMC'
    SSMC = 'SSMC'

    TYPE_CHOICES = (
        (TEXT, 'Text'),
        (NUMBER, 'Number'),
        (NUMBER_RANGE, 'Numeric Range'),
        (MSMC, 'Multi Select'),
        (SSMC, 'Single Select'),
    )
    
    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, blank=True, null=True, related_name='questions')
    name = models.CharField(max_length=200)
    text = models.TextField()
    data_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=SSMC)

    choice_list = models.ForeignKey(
        ChoiceList,
        on_delete=models.CASCADE,
        related_name='questions',
        blank=True,
        null=True
    )
    range_min = models.IntegerField(blank=True, null=True)
    range_max = models.IntegerField(blank=True, null=True)
    range_step = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def data_type_name(self):
        for x in self.TYPE_CHOICES:
            if x[0] == self.data_type:
                return x[1]
        return 'ERROR!'

    def range_params_not_null(self):
        return self.range_min is not None and self.range_max is not None and self.range_step is not None
    
    def can_delete(self):
        if self.surveys.all():
            return False
        if self.answers.all():
            return False
        return True

class MapSurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='surveys')
    sort_order = models.IntegerField(blank=True, null=True)
    
    condition_question = models.ForeignKey('MapSurveyQuestion', on_delete=models.CASCADE, related_name='following', blank=True, null=True)
    condition_answer = models.CharField(max_length=2000, default='', blank=True, null=True)
    
    is_mandatory = models.BooleanField(default=True)
    
    def __str__(self):
        return '{} ! {}'.format(self.survey.name, self.question.name)
        
    def answers(self):
        return self.question.answers.all().filter(survey_instance__survey=self.survey)
    
    def has_condition(self):
        return self.condition_question is not None


class Person(models.Model):

    SEX_M = 'M'
    SEX_F = 'F'
    SEX_CHOICES = (
        (SEX_M, 'Male'),
        (SEX_F, 'Female'),
    )

    email = models.CharField(max_length=200)
    name_first = models.CharField(max_length=100, blank=True, null=True)
    name_second = models.CharField(max_length=100, blank=True, null=True)
    name_last = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.email
        
    def answers(self):
        return Answer.objects.filter(survey_instance__person=self)


class MapUserSurvey(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='surveys')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='persons')
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)
    time_visit = models.DateTimeField(null=True, blank=True)
    random_letters = models.CharField(max_length=5, null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('polls:survey-start', kwargs={'id': self.id, 'secret': self.random_letters})
    
    def generate_random_letters(self):
        letters = 'qwertyuiopasdfghjklzxcvbnm'
        result = ''
        for i in range(5):
            r = int(random.random() * 26.0)
            x = letters[r]
            result += x
        self.random_letters = result
        return

    def save(self, *args, **kwargs):
        if not self.random_letters:
            self.generate_random_letters()
        super(MapUserSurvey, self).save()

    def __str__(self):
        return '{} / {}'.format(self.survey, self.person)


class Answer(models.Model):
    survey_instance = models.ForeignKey(MapUserSurvey, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    data = models.CharField(max_length=2000, blank=True, null=True)
    data_num = models.CharField(max_length=100, blank=True, null=True)
