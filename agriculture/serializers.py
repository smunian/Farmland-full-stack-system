from django.contrib.auth.models import User, Group
from api.models import *

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class SensorMonitor_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorMonitor_info
        fields = '__all__'
