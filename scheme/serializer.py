from rest_framework import serializers
from scheme.models import TblAmcDetails,TblSchemeMaster

class TblAmcDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAmcDetails
        fields = '__all__'

class TblSchemeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblSchemeMaster
        fields = '__all__'