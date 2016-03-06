from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return "%s" % self.name


class Question(models.Model):
    text = models.CharField(max_length=250, null=True, blank=False)
    test = models.ForeignKey(Test)

    def __str__(self):
        return "Question %s for test %s" % (self.text, self.test.name)


class Answer(models.Model):
    text = models.CharField(max_length=150, null=True, blank=False)
    is_right = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return "%s for %s" % (self.text, self.question.text)


class StartedTest(models.Model):
    user = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    questions_number = models.IntegerField(null=False, default=0)
    current_question = models.IntegerField(default=0)
    right_answers = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return "%s for user %s" % self.test.name, self.user.username
