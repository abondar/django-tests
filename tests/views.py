from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from tests.models import *


class TestListView(ListView, LoginRequiredMixin):
    template_name = 'test_list.html'
    model = Test


class TestDetailView(DetailView, LoginRequiredMixin):
    model = Test
    template_name = 'test_detail.html'


class StartTestView(View, LoginRequiredMixin):
    def post(self, request):
        test_id = request.POST['test_id']
        user = request.user

        test = Test.objects.get(id=test_id)
        question_num = Question.objects.filter(test=test).count()
        started_test = StartedTest.objects.create(user=user, test=test, questions_number=question_num)

        return redirect('/test/running/' + str(started_test.id))


class QuestionView(View, LoginRequiredMixin):
    def get(self, request, test_id, **kwargs):
        test = StartedTest.objects.get(id=test_id, user=request.user)
        if test is None or test.is_finished:
            return redirect('/test/')

        if test.current_quetion < test.question_number:
            question = Question.objects.filter(test=test_id)[test.current_quetion]
            test.current_quetion += 1
            test.save()
            return render(request, 'question.html', question)
        else:
            test.is_finished = True
            test.save()
            return redirect('/test/result/' + str(test.id))

    def post(self):
        pass
