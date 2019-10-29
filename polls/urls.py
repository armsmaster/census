from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('choice-list/', views.ChoiceList_List.as_view(), name='choice-list-list'),
    path('choice-list/create/', views.ChoiceList_Create.as_view(), name='choice-list-create'),
    path('choice-list-details/<int:pk>/', views.ChoiceList_Detail.as_view(), name='choice-list-detail'),
    path('question/', views.Question_List.as_view(), name='question-list'),
    path('question/create/', views.Question_Create.as_view(), name='question-create'),
    path('question-details/<int:pk>/', views.Question_Detail.as_view(), name='question-detail'),
    path('question-update/<int:pk>/', views.Question_Update.as_view(), name='question-update'),
    path('question-update/<int:pk>/choice-list/', views.Question_ChoiceList_Update.as_view(), name='question-update-choice-list'),
    path('question-update/<int:pk>/range/', views.Question_Range_Update.as_view(), name='question-update-range'),
    path('survey/', views.Survey_List.as_view(), name='survey-list'),
    path('survey/create/', views.Survey_Create.as_view(), name='survey-create'),
    path('survey-details/<int:pk>/', views.Survey_Detail.as_view(), name='survey-detail'),
    path('survey-update/<int:pk>/', views.Survey_Update.as_view(), name='survey-update'),
    path('survey-update/<int:pk>/add-person/', views.Survey_Detail_Add_Person.as_view(), name='survey-update-add-person'),
    path('person/', views.Person_List.as_view(), name='person-list'),
    path('person/create/', views.Person_Create.as_view(), name='person-create'),
    path('person-details/<int:pk>/', views.Person_Detail.as_view(), name='person-detail'),
    path('person-update/<int:pk>/', views.Person_Update.as_view(), name='person-update'),
    path('survey/<int:id>/<secret>/', views.survey_instance, name='survey-start'),
    path('survey/<int:id>/<secret>/<q>/', views.survey_step, name='survey-step'),
    path('survey-end/<int:id>/<secret>/', views.survey_end, name='survey-end'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
