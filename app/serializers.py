from rest_framework import serializers
from .models import FeederSetting

class FeederSettingSerializer(serializers.ModelSerializer):
    point_value = serializers.ReadOnlyField()
    
    class Meta:
        model = FeederSetting
        fields = ['percentage', 'point_value', 'created_at']



    