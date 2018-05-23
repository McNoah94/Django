from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def redir(request):
    return redirect('/quotes/')

def main(request):#Homepage
    return render(request, 'quotes/index.html')

def validate(request):#Receives errors dictionary from above code and turns it into flash messages, redirects user to previous page if it finds any errors
    errors = User.objects.validator(request.POST)
    if errors:#Generates flash messages
        for key,message in errors.items():
            messages.error(request, message, extra_tags='reg')
        return redirect('/quotes/')
    else:   #If the User successfully registers, website redirects to login page with message
            #declaring successful registration, prompts the User to login via flash message
        User.objects.create(fname=request.POST['fname'], lname=request.POST['lname'],
        email=request.POST['email'],password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()),
        bday=request.POST['bday'])
        messages.success(request, 'Sucessfully registered! Please login.', extra_tags='grn')
        return redirect('/quotes/')

def login(request):#Receives errors dictionary from above code and turns it into flash messages, redirects user to previous page if it finds any errors
    errors = User.objects.login_validator(request.POST)
    if not errors:#There are no errors, email/password validation is done
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):#Email and passwords match
            request.session['user'] = user.id
            return redirect('/quotes/dashboard/')
        else:#Email and passwords don't match
            return redirect('/quotes/')
    else:#There are errors in the form,email/password validation isn't done
        for key,message in errors.items():
            messages.error(request, message, extra_tags='login')
        return redirect('/quotes/')

def dashboard(request):
    context = {
        'user': User.objects.get(id=request.session['user']),
        'all_quotes': Quote.objects.exclude(favorited_by=request.session['user']),
        'my_quotes': User.objects.get(id=request.session['user']).favorite_quotes.all()
    }
    return render(request, 'quotes/dashboard.html', context)

def addQuote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if not errors:
        Quote.objects.create(quoted_by=request.POST['quotedBy'], message=request.POST['message'],
        posted_by=User.objects.get(id=request.session['user']))
        messages.success(request, 'Quote added successfully!', extra_tags='success')
        return redirect('/quotes/dashboard/')
    else:#There are errors in the form
        for key,message in errors.items():
            messages.error(request, message, extra_tags='quote')
        return redirect('/quotes/dashboard/')

def addFav(request, x):
    User.objects.get(id=request.session['user']).favorite_quotes.add(Quote.objects.get(id=x))
    return redirect('/quotes/dashboard/')

def remFav(request, x):
    User.objects.get(id=request.session['user']).favorite_quotes.remove(Quote.objects.get(id=x))
    return redirect('/quotes/dashboard/')

def clear(request):
    request.session.clear()
    return redirect('/quotes/')

def user(request,x):
    context = {
        'user': User.objects.get(id=x),
        'quotes': Quote.objects.filter(posted_by=x),
        'count': Quote.objects.filter(posted_by=x).count()
    }
    return render(request, 'quotes/user.html', context)