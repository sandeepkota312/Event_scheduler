from django.shortcuts import render
from schedule.views import CalendarView
from .models import CustomCalendar,CustomEvent

def calendar_view(request):
    calendars = CustomCalendar.objects.all()  # Retrieve the calendars
    events = CustomEvent.objects.all()  # Retrieve the events
    return render(request, template_name='calendar.html', context={'calendars': calendars, 'events': events})