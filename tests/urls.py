from django.conf.urls import url, include
from tests.views import *

urlpatterns = [
    url(r'^$', TestListView.as_view()),
    url(r'detail/(?P<pk>\w+)/$', TestDetailView.as_view()),
    url(r'^start/$', StartTestView.as_view()),
]
