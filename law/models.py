from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify # new
from django.urls import reverse


class Class_times(models.Model):

    number = models.IntegerField("授業回")
    title = models.CharField("授業タイトル", max_length=255)
    body = models.TextField("概要")

    def __str__(self):
        s = str(self.number) + "回：" + self.title
        return s

    class Meta:
        db_table = 'Class_times'
        verbose_name_plural = '授業回'


class Q_format(models.Model):
    format_name = models.CharField("問題の種類", max_length=255)

    def __str__(self):
        return self.format_name

    class Meta:
        db_table = 'Q_format'
        verbose_name_plural = '問題の種類'


class Question(models.Model):
    title = models.CharField("タイトル", max_length=255)
    class_times = models.ForeignKey(Class_times, on_delete=models.CASCADE, verbose_name="授業回",blank=True,null=True, default=1, related_name='question_field')
    q_format = models.ForeignKey(Q_format, on_delete=models.CASCADE, verbose_name="問題形式")
    slug = models.SlugField(blank=False, unique=True)
    qestion = models.TextField("問題文")
    option1 = models.TextField("選択肢1", blank=True, null=True)
    option2 = models.TextField("選択肢2", blank=True, null=True)
    option3 = models.TextField("選択肢3", blank=True, null=True)
    option4 = models.TextField("選択肢4", blank=True, null=True)
    answer = models.TextField("答え")
    explanation = models.TextField("解説", blank=True, null=True)
    created = models.DateTimeField("作成日時", auto_now_add=True)
    updated = models.DateTimeField("更新日時", auto_now=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('law:ques_practice', kwargs={'slug': self.slug})

    def get_absolute_url_ans(self):
        return reverse('law:ans_ques_practice', kwargs={'slug': self.slug + "/ans"})

    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "Question"
        verbose_name_plural = "問題集"


class User_date(models.Model):
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="ユーザ名")
    class_times = models.ManyToManyField(Class_times, verbose_name="授業回", related_name='user_date_field')
    sum_question = models.IntegerField("問題数", blank=True, null=True)
    created = models.DateTimeField("作成日時", auto_now_add=True)
    updated = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        db_table = "User_date"
        verbose_name_plural = "ユーザの問題検出用データ"


class User_question(models.Model):
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="ユーザ名")
    user_date = models.ForeignKey(User_date, on_delete=models.CASCADE, verbose_name="問題検出用データ", blank=True, null=True)
    q_count = models.IntegerField("問題番号", blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="問題", blank=True, null=True, default=1)
    input_answer = models.TextField("入力値", blank=True, null=True)
    correctness = models.BooleanField("正誤", default=False, blank=True,null=True)
    created = models.DateTimeField("作成日時", auto_now_add=True)
    updated = models.DateTimeField("更新日時", auto_now=True)

    def status(self):
        if self.correctness == True:
            x = "正解"
        else:
            x = "不正解"
        return x

    class Meta:
        db_table = "User_question"
        verbose_name_plural = "ユーザの解答問題"