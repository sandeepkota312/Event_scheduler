from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import Events,EventParticipant
from .serializers import EventSerializer
from django.shortcuts import get_object_or_404

# Create your views here.

def userregister(request):
    if request.user.is_authenticated:
        return redirect(f"/eventsList/{request.user.id}/running/")
    elif request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            # print('user created')
            return redirect("/login/")
    form = NewUserForm()
    return render(request=request, template_name="register.html",
                  context={"register_form": form})

def userlogin(request):
    if request.user.is_authenticated:
        return redirect("eventsList/{request.user.id}/running/")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # print('reached')
                login(request, user)
                return redirect(f'/eventsList/{request.user.id}/running/')
            else:
                print("Invalid username or password.")
        else:
            print("Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})

def userlogout(request):
    logout(request)
    print("You have successfully logged out.")
    return redirect("/")

def my_event(request,id,e_id):
    if request.user.is_authenticated and str(request.user.id)==id:
        event=Events.objects.get(id=int(e_id))
        return render(request=request,template_name='Event_details.html',context={"event":event,"user":request.user})
    else:
        return redirect("/login/")
    
def my_events(request,id):
    if request.user.is_authenticated and str(request.user.id)==id:
        events=Events.get_all_events(user=request.user)
        return render(request=request,template_name='my_events_List.html',context={"events":events,"user":request.user,"length":len(events)})
    else:
        return redirect("/login/")

def running_eventsList(request,id):
    if request.user.is_authenticated and str(request.user.id)==id:
        events=Events.get_running_events(user=request.user)
        return render(request=request,template_name='my_events_List.html',context={"events":events,"user":request.user,"length":len(events)})
    else:
        return redirect("/login/")

def upcoming_eventList(request,id):
    if request.user.is_authenticated and str(request.user.id)==id:
        events=Events.get_upcoming_events(user=request.user)
        return render(request=request,template_name='my_events_List.html',context={"events":events,"user":request.user,"length":len(events)})
    else:
        return redirect("/login/") 

def invited_eventList(request,id):
    if request.user.is_authenticated and str(request.user.id)==id:
        events=EventParticipant.get_invited_events(host_user_id=request.user.id)
        # print('events',len(events))
        return render(request=request,template_name='my_invited_events_List.html',context={"events":events,"user":request.user,"length":len(events)})
    else:
        return redirect("/login/")

def accept_invited_event(request,id,e_id):
    if request.user.is_authenticated and str(request.user.id)==id:
        event=EventParticipant.objects.filter(event=Events.objects.get(id=e_id))
        event.update(status='accepted')
        return redirect(f'/eventsList/{request.user.id}/running/')
    else:
        return redirect("/login/")
def decline_invited_event(request,id,e_id):
    if request.user.is_authenticated and str(request.user.id)==id:
        event=EventParticipant.objects.filter(event=Events.objects.get(id=e_id))
        event.update(status='rejected')
        return redirect(f'/eventsList/{id}/running/')
    else:
        return redirect("/logout/")

def previous_eventList(request,id):
    if request.user.is_authenticated and str(request.user.id)==id:
        events=Events.get_previous_events(user=request.user)
        return render(request=request,template_name='my_events_List.html',context={"events":events,"user":request.user,"length":len(events)})
    else:
        return redirect("/logout/")

def add_event(request,id):
    if request.method=="POST":
        if request.user.is_authenticated and str(request.user.id)==id:
            data={'title':request.POST['Title'],
                'description':request.POST['Content'],
                'start_date_time':request.POST['start_date_time'],
                'end_date_time':request.POST['end_date_time'],
                }
            data['user']=str(request.user.id)
            serializer = EventSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return redirect(f"/eventsList/{request.user.id}/")
            else:
                return render(request=request,template_name="CreateEvent.html")
        else:
            redirect("/logout/")
    else:
        return render(request=request,template_name="CreateEvent.html")

def edit_event(request,id,e_id):
    if str(request.user.id)==id: 
        event=get_object_or_404(Events,id=e_id)
        if request.method=="POST":
            if request.user.is_authenticated:
                event.title=request.POST['Title']
                event.description=request.POST['Content']
                event.start_date_time=request.POST['start_date_time']
                event.end_date_time=request.POST['end_date_time']
                event.save()
                return redirect("/eventsList/" + id +"/")
            else:
                return redirect('/')
        else:
            data={
                'title':event.title,
                'description':event.description,
                'start_date_time':event.start_date_time,
                'end_date_time':event.end_date_time,
                'id':event.id,
            }
            return render(request=request,template_name="EditEvent.html",context=data)
    else:
        return redirect('/logout/')

def invite_participant(request,id,e_id):
    if request.method=="POST":
        if request.user.is_authenticated and str(request.user.id)==id:
            # print('reached till here')
            EventParticipant.invite_user(
                event_id=e_id,
                host_user_id=id,
                invited_username=request.POST['invited_user_id'])
            return redirect(f"/eventsList/{id}/{e_id}")

        else:
            redirect("/logout/")
    else:
        return redirect(f"/eventsList/{id}/{e_id}")

def deleteEvent(request,id,e_id):
    if request.user.is_authenticated and str(request.user.id)==id:
        try:
            event = get_object_or_404(Events, id=e_id)
            event.delete()
            return redirect("/eventsList/<str:id>/")
        except:
            return HttpResponse("post is already deleted")