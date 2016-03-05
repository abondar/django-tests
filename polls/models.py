from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=100)


class Question(models.Model):
    text = models.CharField(max_length=250)
    test = models.ForeignKey(Test)


class Answer(models.Model):
    text = models.CharField(max_length=150)
    is_right = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
