from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, View, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import User_date, Question, User_question
from .forms import ClassTimeForm, UserQuestionForm

TEST_QUESTION = 20

class IndexView(LoginRequiredMixin, TemplateView):

    template_name = 'law/index.html'
    
class SelectionPracticeView(LoginRequiredMixin, CreateView):

    template_name = 'law/selection_practice.html'
    model = User_date
    context_object_name = "UserDate"
    form_class = ClassTimeForm
    success_url = reverse_lazy("law:main_practice")

    def form_valid(self, form):
        userdate = form.save(commit=False)
        userdate.username = self.request.user
        userdate.save()
        User_question.objects.create(
            username = self.request.user,
            user_date = userdate,
            q_count = 1,
            question = Question.objects.filter(class_times__in = form.save().class_times.order_by('?')).order_by('?').first()
        )

        return super().form_valid(form)

class MainPracticeView(LoginRequiredMixin, View):

    form_class = UserQuestionForm

    def get(self,request):
        form = self.form_class()
        model = User_question.objects.filter(username=self.request.user).order_by('-created').first()
        params = {
            "title":model.question.title,
            "quest": model.question.qestion,
            "qcount":model.q_count,
            "form" : form,
        }
        return render(request,'law/main_practice.html',params)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        model = User_question.objects.filter(username=self.request.user).order_by('-created').first()
        if form.is_valid():
            date = form.save(commit=False)
            model.input_answer = date.input_answer
            model.save()
            return HttpResponseRedirect("ans_practice")

class AnsPracticeView(LoginRequiredMixin, View):

    template_name = 'law/ans_practice.html'

    def get(self,request):
        model = User_question.objects.filter(username=self.request.user).order_by('-created').first()
        if model.input_answer == model.question.answer:
            y = True
        else:
            y = False
        model.correctness = y
        model.save()
        if model.q_count < model.user_date.sum_question:
            slug = "main_practice"
            create = True
        else:
            slug = "finish_practice"
            create = False
        params = {
            "title":model.question.title,
            "quest": model.question.qestion,
            "answer" : model.input_answer,
            "kaitou": model.status(),
            "kai" : model.question.answer,
            'exp' : model.question.explanation,
            "slug" : slug,
        }
        if create:
            User_question.objects.create(
                username = self.request.user,
                user_date = model.user_date,
                q_count = model.q_count + 1,
                question = Question.objects.filter(class_times__in = model.user_date.class_times.order_by('?')).order_by('?').first()
            )
        return render(request,'law/ans_practice.html',params)

class FhishPracticeView(LoginRequiredMixin, TemplateView):
    
    def get(self,request):
        count = User_date.objects.filter(username=self.request.user).order_by('-created').first().sum_question
        model = User_question.objects.filter(username=self.request.user).order_by('-created')[:count]
        params = {
            "models":model
        }
        return render(request,"law/finish_practice.html",params)
    
class QuestionPracticeView(LoginRequiredMixin, FormView, DetailView):

    template_name = "law/ques_practice.html"
    model = Question
    context_object_name = "question"
    form_class = UserQuestionForm
    
    
    def get_success_url(self):
        return reverse('law:ans_ques_practice', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super(QuestionPracticeView, self).get_context_data(**kwargs)
        form = self.get_form()
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        User_question.objects.create(
            username = self.request.user,
            user_date = User_date.objects.filter(username=self.request.user).order_by('-created').first(),
            q_count = 0,
            question = Question.objects.filter(slug=self.kwargs['slug']).first(),
            input_answer = form['input_answer'].value(),
        )
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form):
        return super(QuestionPracticeView, self).form_valid(form)

class QuestionAnsPracticeView(LoginRequiredMixin, DetailView):

    template_name = 'law/ans_ques_practice.html'
    model = Question
    context_object_name = "question"

    def get(self,request, slug):
        x = User_question.objects.filter(username=self.request.user).order_by('-created').first()
        if x.input_answer == x.question.answer:
            y = True
        else:
            y = False
        x.correctness = y
        x.save()
        params = {
            "model": x,
        }
        return render(request,'law/ans_ques_practice.html',params)


class TestView(LoginRequiredMixin, ListView):

    template_name = 'law/test.html'
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'models' : Question.objects.order_by('?')[:TEST_QUESTION]
        }
        return context

class ListQuestionView(LoginRequiredMixin, ListView):

    template_name = 'law/list.html'
    model = User_question
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'models' : User_question.objects.filter(username=self.request.user).order_by('-created').all()
        }
        return context