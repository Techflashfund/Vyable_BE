from rest_framework import serializers
from scheme.models import TblAmcDetails,TblSchemeMaster,TblNavHistoryMaster, TblNavMaster, TblSchemeDetails

class TblAmcDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblAmcDetails
        fields = '__all__'

class TblSchemeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblSchemeMaster
        fields = '__all__'

class TblNavHistoryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblNavHistoryMaster
        fields = '__all__'


class TblNavMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblNavMaster
        fields = '__all__'

class TblSchemeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblSchemeDetails
        fields = '__all__'