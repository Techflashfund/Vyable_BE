from django.urls import path
from .views import *


urlpatterns=[
    path('amc-details/', AMCListView.as_view(), name='amc-details'),
    path('scheme/', SchemeListView.as_view(), name='scheme-details'),
    path('nav-history/', NAVHistoryListView.as_view(), name='nav-history'),
    path('nav-master/', NAVMasterListView.as_view(), name='nav-master'),
    path('scheme-details/', SchemeDetailsListView.as_view(), name='scheme-details'),
]