from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from tests.models import *


class TestListView(LoginRequiredMixin, ListView):
    template_name = 'test_list.html'
    model = Test



