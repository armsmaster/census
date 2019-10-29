from django.contrib import admin
from .models import ChoiceList
from .models import Choice
from .models import Question
from .models import Survey
from .models import MapSurveyQuestion
from .models import Person
from .models import MapUserSurvey
from .models import Answer


admin.site.register(ChoiceList)
admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(MapSurveyQuestion)
admin.site.register(Person)
admin.site.register(MapUserSurvey)
admin.site.register(Answer)
