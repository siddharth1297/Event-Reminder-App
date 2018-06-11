from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import LoginForm, SignupForm, NewEvent
from django.forms import Form
from django.contrib.auth.models import User
from .models import UserProfile, ToDo
import datetime
from django.urls import reverse
from django.contrib.auth.views import login

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('to_do', args=[request.user]))
    return render(request, 'index.html')


def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('to_do', args=[request.user]))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            print(username + password)
            user = authenticate(username=username, password=password)
            if user is None:
                print(user)
                return render(request, 'login.html', {'instruction': 'Enter valid username and password', 'form': form})
            login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect(reverse('to_do', args=[username]))
        return render(request, 'login.html', {'instruction': 'Enter valid data', 'form': form})
    form = LoginForm()
    return render(request, 'login.html', {'instruction': 'WELCOME', 'form': form})


def user_signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('to_do', args=[request.user]))
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            email    = data['email']
            phone    = data['phone']
            gender   = data['gender']
            print(username + password + email + str(phone) + gender)
            try:
                if len(User.objects.filter(email=email)) is not 0:
                    return render(request, 'signup.html', {'instruction': 'user with email already exist. Try other email', 'form': form})

                user = User.objects.create_user(username=username, password=password, is_staff=True)
                user.email = email
                user.save()
                print('user save')
            except:
                return render(request, 'signup.html',
                              {'instruction': 'user with username already exist. Try other name', 'form': SignupForm()})
            try:
                print('userprofile')
                userprofile = UserProfile(username=user, phone=phone, gender=gender)
                userprofile.save()
                print('userprofile save')
            except:
                User.objects.filter(username=username).delete()
                return render(request, 'signup.html', {'instruction': 'user with phone number already exist. Try other name', 'form': SignupForm()})

            print('all successful')
            return redirect('/login')
        else:
            return render(request, 'signup.html', {'instruction': 'Enter valid data', 'form':form})

    form = SignupForm()
    return render(request, 'signup.html', {'instruction': 'WELCOME', 'form':form})


@login_required
def to_do(request, username):
    if request.user.is_authenticated == False or username != request.session['username']:
        return HttpResponseRedirect(reverse('Login'))
    print(username)
    print('session' + request.session['username'])
    user = User.objects.get(username=username)
    print(username)
    #get all events
    all_events = ToDo.objects.filter(username=user).order_by('event_time')
    NewEventForm = NewEvent()
    return render(request, 'todo.html', {'username': username, 'all_events': all_events, 'form': NewEventForm})

@login_required
def Delete(request, username, id):
    print(id)
    user = User.objects.get(username=username)
    ToDo.objects.filter(id=int(id)).delete()
    return HttpResponseRedirect(reverse('to_do', args=[username]))

@require_POST
def AddEvent(request, username):
    new_event_form = NewEvent(request.POST)
    if new_event_form.is_valid():
        data = new_event_form.cleaned_data
        events = data['events']
        event_date   = data['event_date']
        event_time   = data['event_time']
        sms_date = data['sms_date']
        sms_time = data['sms_time']
        print(username)
        print(events)
        print(str(event_time))
        print(str(event_date))
        event_datetime = datetime.datetime.combine(event_date, event_time)
        sms_datetime = datetime.datetime.combine(sms_date, sms_time)
        print(event_datetime)
        print(sms_datetime)

        user = User.objects.get(username=username)
        event_new_object = ToDo(username=user, events=events, event_time=event_datetime, sms_time=sms_datetime, is_completed=False)
        event_new_object.save()
        return HttpResponseRedirect(reverse('to_do', args=[username]))


@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login'))