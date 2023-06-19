from django.urls import path
from . import views

urlpatterns = [
    # path('', views.hello, name="Hello"),
    path('', views.userregister, name="user-register"),
    path('login/', views.userlogin, name="user-login"),
    path('logout/', views.userlogout, name="user-logout"),
    path('eventsList/<str:id>/',views.my_events,name='My events'),
    path('eventsList/<str:id>/invited/',views.invited_eventList,name='Invited events'), #eventsList/{{ user.id }}/invited/accept/
    path('eventsList/<str:id>/invited/<str:e_id>/accept/',views.accept_invited_event,name='accept Invited event'),
    path('eventsList/<str:id>/invited/<str:e_id>/decline/',views.decline_invited_event,name='decline Invited event'),
    path('eventsList/<str:id>/running/',views.running_eventsList,name='Running events'),
    path('eventsList/<str:id>/previous/',views.previous_eventList,name='Previous events'),
    path('eventsList/<str:id>/upcoming/',views.upcoming_eventList,name='Upcoming events'),
    path('eventsList/<str:id>/eventcreate/',views.add_event,name="Add event"),
    path('eventsList/<str:id>/<str:e_id>/',views.my_event,name='My event'),
    path('eventsList/<str:id>/<str:e_id>/edit/',views.edit_event,name='Edit event'),
    path('eventsList/<str:id>/<str:e_id>/invite/',views.invite_participant,name="invite participant"),
    path('eventsList/<str:id>/<str:e_id>/delete/', views.deleteEvent, name="deletepost"),
]