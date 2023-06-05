# Create your models here.
from django.db import models
from schedule.models import Event, Calendar

class CustomCalendar(Calendar):
    # Add any additional fields or customizations specific to your 
    pass
class CustomEvent(Event):
    pass
