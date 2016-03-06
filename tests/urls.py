from django.conf.urls import url, include
from tests.views import *

urlpatterns = [
    url(r'', TestListView.as_view()),
]
