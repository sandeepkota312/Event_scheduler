# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class EventAbstract(models.Model):
    """ Event abstract model """
    id = models.BigAutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    # is_deleted = models.BooleanField(default=False)
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
        events = Events.objects.filter(user=user).order_by('-start_date_time')
        return events

    def get_running_events(user):
        running_events = Events.objects.filter(
            user=user,
            is_active=True,
            # is_deleted=False,
            start_date_time__lte=datetime.now(),
            end_date_time__gte=datetime.now()
        ).order_by("start_date_time")

        accepted_events=EventParticipant.objects.filter(
            user=user,
            status='accepted',
        )
        running_events=list(running_events)
        for event in accepted_events:
            if event.event.start_date_time<=timezone.now() and event.event.end_date_time>=timezone.now():
                running_events.append(event.event)

        prev_events=Events.objects.filter(
            user=user,
            is_active=True,
            # is_deleted=False,
            end_date_time__lte=datetime.now()
        ).order_by("start_date_time")
        prev_events.update(is_active=False)
        return running_events
    
    def get_previous_events(user):
        prev_events=Events.objects.filter(
            user=user,
            # is_deleted=False,
            end_date_time__lte=datetime.now()
        ).order_by("start_date_time")
        prev_events.update(is_active=False)

        accepted_events=EventParticipant.objects.filter(
            user=user,
            status='accepted',
        )
        prev_events=list(prev_events)
        for event in accepted_events:
            if event.event.is_active==False:
                prev_events.append(event.event)
        return prev_events
    
    def get_upcoming_events(user):
        upcoming_events=Events.objects.filter(
            user=user,
            # is_deleted=False,
            start_date_time__gte=datetime.now()
        ).order_by("start_date_time")

        accepted_events=EventParticipant.objects.filter(
            user=user,
            status='accepted',
        )
        upcoming_events=list(upcoming_events)
        for event in accepted_events:
            if event.event.start_date_time>=timezone.now():
                # print(event.event.start_date_time)
                # print(timezone.now())
                upcoming_events.append(event.event)
        # print(upcoming_events)
        return upcoming_events

    def __str__(self):
        return f"{self.user} is invited for {self.title}"
    
class EventParticipant(models.Model):
    # event = models.ForeignKey(Events.id, on_delete=models.CASCADE) need to implement this at the end
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
    
    def get_invited_events(host_user_id):
        IDs=EventParticipant.objects.filter(user=User.objects.get(id=host_user_id),status='invited')
        print('ids',IDs)
        invited_list=[]
        for id in IDs:
            invited_list.append(id.event)
        print('invted',invited_list)
        return invited_list

    def get_accepted_user_list(self,event_id,host_user_id):
        event=Events.objects.get(id=event_id)
        if event.user.id == host_user_id:
            IDs=EventParticipant.objects.filter(event=event,status='accepted')
            accepted_list=[]
            for id in IDs:
                accepted_list.append(id.user)
            return accepted_list
        return []
    
    def get_rejected_user_list(self,event_id,host_user_id):
        event=Events.objects.get(id=event_id)
        if event.user.id == host_user_id:
            IDs=EventParticipant.objects.filter(event=event,status='accepted')
            accepted_list=[]
            for id in IDs:
                accepted_list.append(id.user)
            return accepted_list
        return []
    
    @staticmethod
    def invite_user(event_id, host_user_id, invited_username):
        invited_user=User.objects.get(username=invited_username)
        # print(invited_user.username,invited_user.id)
        event = Events.objects.get(id=event_id)
        if str(event.user.id) == host_user_id:
            EventParticipant.objects.create(event=event, user=invited_user)
        else:
            print('something went wrong')
