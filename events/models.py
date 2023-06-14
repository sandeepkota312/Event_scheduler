# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import datetime

class EventAbstract(models.Model):
    """ Event abstract model """
    id = models.BigAutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Events(EventAbstract):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)

    title=models.CharField(max_length=50)
    description = models.TextField()

    start_date_time=models.DateTimeField()
    end_date_time=models.DateTimeField()

    def get_all_events(user):
        events = Events.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(user):
        running_events = Events.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events
    
    def __str__(self):
        return f"{self.user}-{self.title}"
    
class EventParticipant(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    STATUS_CHOICES = (
        ('invited', 'Invited'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='invited')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    
    def get_invited_events(self,host_user):
        events_list=EventParticipant.objects.get(user=host_user).event
        # events_list=[]
        # for id in ids:
        #     events_list.append(Events.objects.get(id=id))
        return events_list

    @staticmethod
    def invite_user(event_id, host_user, invited_user):
        event = Events.objects.get(id=event_id)
        if event.host == host_user:
            EventParticipant.objects.create(event=event, user=invited_user)
