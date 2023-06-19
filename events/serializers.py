from rest_framework import serializers
from .models import Events,EventParticipant
from django.contrib.auth.models import User
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Events
        fields=['user','id','title','description','start_date_time','end_date_time']

# class EventParticipantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=EventParticipant
#         fields=[]



