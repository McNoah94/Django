from django.db import models
from django.core.validators import validate_email, ValidationError

import datetime

class UserManager(models.Manager):
    def validator(self, form):
        errors = {}
        for i in form:
            if not i:
                errors['empty'] = 'One of your fields are empty jackass'
        if len(form['email']) < 1:
            errors['email'] = 'Your email is empty bro'
        elif not validateEmail(form['email']):
            errors['invalid'] = "Your email doesn't appear valid"
        elif form['password'] != form['confirm']:
            errors['pass'] = "Passwords don't match"
        elif len(form['lname']) > 15 or len(form['fname']) > 15:
            errors['name'] = 'Name fields can have up to 15 characters'
        elif not form['fname'].isalpha() or not form['lname'].isalpha():
            errors['name'] = "Name fields can't have any numbers in them"
        return errors
    
    def login_validator(self, form):
        errors = {}
        print('running')
        if len(form['email']) < 1:
            errors['email'] = 'Empty field'
            print('empty field detected')
        elif len(form['email']) > 1:
            try:
                User.objects.get(email=form['email'])
            except:
                errors['exist'] = "Email is not registered"
        return errors

class TripManager(models.Manager):
    def trip_validator(self, form):
        errors = {}
        if not form['from'] or not form['to'] or not form['name'] or not form['desc']:
            errors['empty'] = 'One or more fields is empty!'
        elif form['from'] > form['to']:
            errors['date'] = 'FROM date must be set to before TO date!'
        return errors


class User(models.Model):
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "{}: {} {}".format(self.id, self.fname, self.lname)


class Trip(models.Model):
    name = models.CharField(max_length=60)
    desc = models.CharField(max_length=60)
    created_by = models.ForeignKey(User, related_name='trips_created')
    travellers = models.ManyToManyField(User, related_name='trips_joined')
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    def __repr__(self):
        return "{}, {}, {} to {}".format(self.name, self.desc, self.date_from, self.date_to)


def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False