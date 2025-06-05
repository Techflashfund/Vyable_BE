from django.urls import path
from .views import *


urlpatterns=[
    path('amc-details/', AMCListView.as_view(), name='amc-details'),
    path('scheme-details/', SchemeListView.as_view(), name='scheme-details'),
]