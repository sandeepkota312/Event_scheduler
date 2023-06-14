from django.contrib import admin
from .models import EventParticipant,Events
# Register your models here.
admin.site.register(Events)
admin.site.register(EventParticipant)
