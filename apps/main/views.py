from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Trip
import bcrypt

def main(request):
    return render(request, 'main/index.html')

def validate(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for key,message in errors.items():
            messages.error(request, message, extra_tags='reg')
        return redirect('/main/')
    else:   #If the User successfully registers, website redirects to login page with message prompting
            #the User to login via flash message
        User.objects.create(fname=request.POST['fname'], lname=request.POST['lname'],
        email=request.POST['email'],password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        messages.success(request, 'Sucessfully registered! Please login.', extra_tags='grn')
        return redirect('/main/')

def travels(request):
    context = {
        'user': User.objects.get(id=request.session['user']),
        'my_trips': User.objects.get(id=request.session['user']).trips_joined.all(),
        'all_trips': Trip.objects.exclude(travellers=request.session['user'])
    }
    return render(request, 'main/travels.html/', context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    print('just called')
    if not errors:
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user'] = user.id
            return redirect('/main/travels/')
        else:
            return redirect('/main/')
    else:
        for key,message in errors.items():
            messages.error(request, message, extra_tags='login')
        return redirect('/main/')

def add(request):
    return render(request, 'main/add.html')

def logout(request):
    request.session.clear()
    return redirect('/main/')

def newPlan(request):
    errors = Trip.objects.trip_validator(request.POST)
    if not errors:
        Trip.objects.create(name=request.POST['name'], desc=request.POST['desc'],
        created_by=User.objects.get(id=request.session['user']), date_from=request.POST['from'],
        date_to=request.POST['to'])
        return redirect('/main/travels/')
    else:
        for key,message in errors.items():
            messages.error(request, message, extra_tags=key)
            return redirect('/main/travels/add/')

def showTrip(request, x):
    context = {
        'trip': Trip.objects.get(id=x),
        'travellers': Trip.objects.get(id=x).travellers.all()
    }
    return render(request, 'main/show.html', context)

def join(request, x):
    Trip.objects.get(id=x).travellers.add(User.objects.get(id=request.session['user']))
    return redirect('/main/travels/')