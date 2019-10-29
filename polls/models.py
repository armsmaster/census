from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random


class Survey(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class ChoiceList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Choice(models.Model):
    choice_list = models.ForeignKey(ChoiceList, on_delete=models.CASCADE, related_name='choices')
    name = models.CharField(max_length=500)

    def __str__(self):
        return '[{}] ! {}'.format(self.choice_list.name, self.name)


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
        (MSMC, 'Multi Select Multiple Choice'),
        (SSMC, 'Single Select Multiple Choice'),
    )

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


class MapSurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='surveys')
    sort_order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} ! {}'.format(self.survey.name, self.question.name)


class Person(models.Model):

    SEX_M = 'M'
    SEX_F = 'F'
    SEX_CHOICES = (
        (SEX_M, 'М'),
        (SEX_F, 'Ж'),
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


class MapUserSurvey(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='surveys')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='persons')
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)
    time_visit = models.DateTimeField(null=True, blank=True)
    random_letters = models.CharField(max_length=5, null=True, blank=True)

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
        return '{} ! {}'.format(self.person, self.survey)


class Answer(models.Model):
    survey_instance = models.ForeignKey(MapUserSurvey, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    data = models.CharField(max_length=2000, blank=True, null=True)
