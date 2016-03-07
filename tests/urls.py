from django.conf.urls import url, include
from tests.views import *

urlpatterns = [
    url(r'^$', TestListView.as_view()),
    url(r'detail/(?P<pk>\w+)/$', TestDetailView.as_view()),
    url(r'start/$', StartTestView.as_view()),
    url(r'running/(?P<test_id>\w+)/$', QuestionView.as_view()),
    url(r'result/(?P<test_id>\w+)/$', ResultView.as_view()),
]
