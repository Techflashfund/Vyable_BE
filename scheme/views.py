from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response    
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import TblAmcDetails,TblSchemeMaster,TblNavHistoryMaster
from .serializer import *
from django_filters.rest_framework import DjangoFilterBackend


class AMCListView(ListAPIView):
    """
    View to list all AMC details from dump_db.
    """
    serializer_class = TblAmcDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['amc_code', 'amc_name']

    def get_queryset(self):
        return TblAmcDetails.objects.using('dump_db').all()
    
class SchemeListView(ListAPIView):
    """
    View to list all Scheme details from dump_db.
    """
    serializer_class = TblSchemeDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def get_queryset(self):
        return TblSchemeMaster.objects.using('dump_db').all()


class NAVHistoryListView(ListAPIView):
    """
    View to list all NAV history details from dump_db.
    """
    serializer_class = TblNavHistoryMasterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["isin",'nav_date','nav_value']

    def get_queryset(self):
        return TblNavHistoryMaster.objects.using('dump_db').all()

class NAVMasterListView(ListAPIView):
    """
    View to list NAV Master records from dump_db.
    """
    queryset = TblNavMaster.objects.using('dump_db').all()
    serializer_class = TblNavMasterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['isin', 'scheme_code', 'scheme_name', 'nav_date']

class SchemeDetailsListView(ListAPIView):
    """
    View to list Scheme Details from dump_db.
    """
    queryset = TblSchemeDetails.objects.using('dump_db').all()
    serializer_class = TblSchemeDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['isin', 'fund_type', 'riskometer', 'category', 'fund_manager']
    