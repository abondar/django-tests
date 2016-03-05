from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from polls.models import *


class TestListView(ListView):
    template_name = 'test_list.html'
    model = Test
