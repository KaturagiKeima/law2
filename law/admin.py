from django.contrib import admin
from .models import Class_times, Q_format, Question, User_date, User_question

admin.site.register(Class_times)
admin.site.register(Q_format)
admin.site.register(Question)
admin.site.register(User_date)
admin.site.register(User_question)

# Register your models here.
