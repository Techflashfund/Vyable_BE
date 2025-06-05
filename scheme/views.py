from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response    
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import TblAmcDetails,TblSchemeMaster
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

    