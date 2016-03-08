from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from tests.models import *


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'test_list.html'


class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'test_detail.html'


class StartTestView(LoginRequiredMixin, View):
    def post(self, request):
        test_id = request.POST['test_id']
        user = request.user

        test = Test.objects.get(id=test_id)
        question_num = Question.objects.filter(test=test).count()
        started_test = StartedTest.objects.create(user=user, test=test, questions_number=question_num)

        return redirect('/test/running/' + str(started_test.id))


class QuestionView(LoginRequiredMixin, View):
    def get(self, request, test_id, **kwargs):
        test = StartedTest.objects.get(id=test_id, user=request.user)

        if test is None or test.is_finished:
            return redirect('/test/')

        return self.render_current_question(request, test)

    def post(self, request, test_id):
        answer_list = request.POST.getlist('answer')
        test = StartedTest.objects.get(id=test_id, user=request.user)

        if test is None or test.is_finished:
            return redirect('/test/')

        question = Question.objects.filter(test=test.test)[test.current_question]

        chosen_answers = Answer.objects.filter(id__in=answer_list)
        right_answers = Answer.objects.filter(question=question, is_right=True)

        if list(chosen_answers) == list(right_answers):
            test.right_answers += 1
        test.current_question += 1
        test.save()

        return self.render_current_question(request, test)

    def render_current_question(self, request, test):
        if test.current_question < test.questions_number:
            question = Question.objects.filter(test=test.test)[test.current_question]
            progress = int((test.current_question / test.questions_number) * 100)
            return render(request, 'question.html', {'question': question, 'test': test, 'progress': progress})
        else:
            test.is_finished = True
            test.save()
            return redirect('/test/result/' + str(test.id))


class ResultView(LoginRequiredMixin, View):
    def get(self, request, test_id):
        test = StartedTest.objects.get(id=test_id, user=request.user)

        if test is None:
            return redirect('/test/')

        percent = int((test.right_answers / test.questions_number) * 100)
        return render(request, "result.html", {'test': test, 'percent': percent})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        test_list = StartedTest.objects.filter(user=request.user, is_finished=True)
        return render(request, "profile.html", {'user': request.user, 'test_list': test_list})
