from django.urls import path
from . import views

app_name = 'law'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('selection_practice', views.SelectionPracticeView.as_view(), name='selection_practice'),
    path('test', views.TestView.as_view(), name='test'),
    path('list', views.ListQuestionView.as_view(), name='list'),
    path('main_practice', views.MainPracticeView.as_view(), name="main_practice"),
    path('ans_practice', views.AnsPracticeView.as_view(), name='ans_practice'),
    path('finish_practice',views.FhishPracticeView.as_view(), name='finish_practice'),
    path('<slug:slug>', views.QuestionPracticeView.as_view(), name='ques_practice'),
    path('<slug:slug>/ans', views.QuestionAnsPracticeView.as_view(), name='ans_ques_practice'),
    
]