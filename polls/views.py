import datetime
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from . import forms


class ChoiceList_List(LoginRequiredMixin, generic.ListView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.ChoiceList
    template_name = 'polls/choice_list_list.html'
    context_object_name = 'items'


class ChoiceList_Detail(LoginRequiredMixin, generic.DetailView, generic.FormView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.ChoiceList
    template_name = 'polls/choice_list_detail.html'
    form_class = forms.Choice_Form

    def get_success_url(self):
        object = self.get_object()
        return '/polls/choice-list-details/{}/'.format(object.id)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        choice = form.save(commit=False)
        choice.choice_list = self.get_object()
        choice.save()
        return super(ChoiceList_Detail, self).form_valid(form)


class ChoiceList_Create(LoginRequiredMixin, generic.edit.CreateView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.ChoiceList
    fields = ['name']
    template_name = 'polls/choice_list_create.html'

    def get_success_url(self):
        return reverse('polls:choice-list-detail', kwargs={'pk': self.object.pk})


class Question_List(LoginRequiredMixin, generic.ListView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Question
    template_name = 'polls/question_list.html'
    context_object_name = 'items'


class Question_Detail(LoginRequiredMixin, generic.DetailView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Question
    template_name = 'polls/question_detail.html'


class Question_Create(LoginRequiredMixin, generic.edit.CreateView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Question
    fields = ['name', 'text', 'data_type']
    template_name = 'polls/question_create.html'

    def get_success_url(self):
        return reverse('polls:question-detail', kwargs={'pk': self.object.pk})


class Question_Update(LoginRequiredMixin, generic.UpdateView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Question
    fields = ['name', 'text', 'data_type']
    template_name = 'polls/question_update.html'

    def get_success_url(self):
        return reverse('polls:question-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if form.instance.data_type in [models.Question.MSMC, models.Question.SSMC]:
            form.instance.range_min = None
            form.instance.range_max = None
            form.instance.range_step = None
        elif form.instance.data_type == models.Question.NUMBER_RANGE:
            form.instance.choice_list = None
        elif form.instance.data_type in [models.Question.TEXT, models.Question.NUMBER]:
            form.instance.range_min = None
            form.instance.range_max = None
            form.instance.range_step = None
            form.instance.choice_list = None
        return super().form_valid(form)


class Question_ChoiceList_Update(LoginRequiredMixin, generic.UpdateView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Question
    fields = ['choice_list']
    template_name = 'polls/question_update.html'

    def get_success_url(self):
        return reverse('polls:question-detail', kwargs={'pk': self.object.pk})


class Question_Range_Update(LoginRequiredMixin, generic.UpdateView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Question
    fields = ['range_min', 'range_max', 'range_step']
    template_name = 'polls/question_update.html'

    def get_success_url(self):
        return reverse('polls:question-detail', kwargs={'pk': self.object.pk})


class Survey_List(LoginRequiredMixin, generic.ListView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Survey
    template_name = 'polls/survey_list.html'
    context_object_name = 'items'


class Survey_Detail(LoginRequiredMixin, generic.DetailView, generic.FormView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Survey
    template_name = 'polls/survey_detail.html'
    form_class = forms.MapSurveyQuestion_Form

    def get_success_url(self):
        object = self.get_object()
        return '/polls/survey-details/{}/'.format(object.id)

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msq = form.save(commit=False)
        msq.survey = self.get_object()
        msq.save()
        return super(Survey_Detail, self).form_valid(form)


class Survey_Detail_Add_Person(LoginRequiredMixin, generic.DetailView, generic.FormView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Survey
    template_name = 'polls/survey_detail_add_person.html'
    form_class = forms.MapUserSurvey_Form

    def get_success_url(self):
        object = self.get_object()
        return '/polls/survey-details/{}/'.format(object.id)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msp = form.save(commit=False)
        msp.survey = self.get_object()
        msp.save()
        return super(Survey_Detail_Add_Person, self).form_valid(form)


class Survey_Create(LoginRequiredMixin, generic.edit.CreateView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Survey
    fields = ['name', 'description']
    template_name = 'polls/survey_create.html'

    def get_success_url(self):
        return reverse('polls:survey-detail', kwargs={'pk': self.object.pk})


class Survey_Update(LoginRequiredMixin, generic.UpdateView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Survey
    fields = ['name', 'description']
    template_name = 'polls/survey_update.html'

    def get_success_url(self):
        return reverse('polls:survey-detail', kwargs={'pk': self.object.pk})



class Person_List(LoginRequiredMixin, generic.ListView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Person
    template_name = 'polls/person_list.html'
    context_object_name = 'items'


class Person_Detail(LoginRequiredMixin, generic.DetailView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Person
    template_name = 'polls/person_detail.html'


class Person_Create(LoginRequiredMixin, generic.edit.CreateView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Person
    fields = ['email', 'name_first', 'name_second', 'name_last', 'birth_date', 'sex', 'title']
    template_name = 'polls/person_create.html'

    def get_success_url(self):
        return reverse('polls:person-detail', kwargs={'pk': self.object.pk})


class Person_Update(LoginRequiredMixin, generic.UpdateView):
    login_url = '/polls/login/'
    redirect_field_name = 'next'
    model = models.Person
    fields = ['email', 'name_first', 'name_second', 'name_last', 'birth_date', 'sex', 'title']
    template_name = 'polls/person_update.html'

    def get_success_url(self):
        return reverse('polls:person-detail', kwargs={'pk': self.object.pk})


def survey_instance(request, **kwargs):
    template = loader.get_template('polls/survey_start.html')
    survey_id = kwargs.get('id', None)
    secret_code = kwargs.get('secret', None)

    if not survey_id:
        return

    if not secret_code:
        return

    surv = models.MapUserSurvey.objects.filter(pk=survey_id).first()

    if not surv:
        return

    if surv.random_letters != secret_code:
        return

    if not surv.time_visit:
        surv.time_visit = datetime.datetime.now()
        surv.save()

    all_q = surv.survey.questions.all().order_by('id')
    if not all_q:
        next_q = -1
    else:
        next_q = all_q[0]

    context = {
        'object': surv,
        'next_q': next_q,
    }
    return HttpResponse(template.render(context, request))


def survey_step(request, **kwargs):
    template = loader.get_template('polls/survey_step.html')
    survey_id = kwargs.get('id', None)
    secret_code = kwargs.get('secret', None)
    q = kwargs.get('q', None)

    if not survey_id:
        return

    if not secret_code:
        return

    if not q:
        return

    surv = models.MapUserSurvey.objects.filter(pk=survey_id).first()

    if not surv:
        return

    if surv.random_letters != secret_code:
        return

    all_q = surv.survey.questions.all().order_by('id')
    if not all_q:
        return

    q_current = all_q.filter(id=q).first()

    if not q_current:
        return

    if not surv.time_start:
        surv.time_start = datetime.datetime.now()
        surv.save()

    all_q_next = all_q.filter(id__gt=q).order_by('id')

    if not all_q_next:
        next_q = None
    else:
        next_q = all_q_next[0]
    
    choices_x = ((1, 'one'), (2, 'two'))
    
    if request.method == "POST":
        if q_current.question.data_type == models.Question.MSMC:
            form = forms.MSMC(request.POST)
            choices = [(c.id, c.name) for c in q_current.question.choice_list.choices.all()]
            form.fields['data'].choices = choices
            print('xxxxxx')
            if form.is_valid():
                print(form.cleaned_data['data'])
            
        if q_current.question.data_type == models.Question.SSMC:
            form = forms.SSMC(request.POST)
            print(form)
            choices = [('x' + str(c.id), c.name) for c in q_current.question.choice_list.choices.all()]
            form.fields['data'].choices = choices
            print('xxxxxx')
            j = form.is_valid()
            print(j)
            for k, v in form.fields['data'].choices:
                print(k, ',', v, ',', isinstance(v, (list, tuple)))
            if form.is_valid():
                print(form.cleaned_data['data'])
        
        if next_q:
            return HttpResponseRedirect(reverse('polls:survey-step', kwargs={'id': surv.pk, 'secret': surv.random_letters, 'q': next_q.pk}))
        else:
            return HttpResponseRedirect(reverse('polls:survey-end', kwargs={'id': surv.pk, 'secret': surv.random_letters}))
    
    form = None
    
    if q_current.question.data_type == models.Question.MSMC:
        choices = [(c.id, c.name) for c in q_current.question.choice_list.choices.all()]
        form = forms.MSMC()
        form.fields['data'].choices  = choices
    if q_current.question.data_type == models.Question.SSMC:
        choices = [('x' + str(c.id), c.name) for c in q_current.question.choice_list.choices.all()]
        form = forms.SSMC()
        form.fields['data'].choices  = choices
    
    context = {
        'object': surv,
        'q_current': q_current,
        'form': form,
        'next_q': next_q,
    }
    return HttpResponse(template.render(context, request))


def survey_end(request, **kwargs):
    template = loader.get_template('polls/survey_end.html')
    survey_id = kwargs.get('id', None)
    secret_code = kwargs.get('secret', None)

    if not survey_id:
        return

    if not secret_code:
        return

    surv = models.MapUserSurvey.objects.filter(pk=survey_id).first()

    if not surv:
        return

    if surv.random_letters != secret_code:
        return

    if not surv.time_end:
        surv.time_end = datetime.datetime.now()
        surv.save()

    context = {
        'object': surv,
    }
    return HttpResponse(template.render(context, request))
