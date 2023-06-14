from django.urls import path
from . import views

urlpatterns = [
    # path('', views.hello, name="Hello"),
    path('', views.userregister, name="user-register"),
    path('login/', views.userlogin, name="user-login"),
    path('logout/', views.userlogout, name="user-logout"),
    path('eventsList/',views.eventsList,name='my events'),
]