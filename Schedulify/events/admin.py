from django.contrib import admin
from .models import CustomCalendar,CustomEvent
# Register your models here.
admin.site.register(CustomCalendar)
admin.site.register(CustomEvent)
