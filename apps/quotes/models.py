from django.db import models
from django.core.validators import validate_email, ValidationError
from datetime import datetime
from time import strptime

class UserManager(models.Manager):
    def validator(self, form):
        errors = {}
        if len(form['email']) < 1:
            errors['email'] = 'Your email is empty'
        if len(form['fname']) < 1 or len(form['lname']) < 1:
            errors['name'] = 'One of your name fields is empty'
        elif not form['fname'].isalpha() or not form['lname'].isalpha():
            errors['name'] = "Name fields can't have any numbers in them"
        elif not validateEmail(form['email']):
            errors['invalid'] = "Your email doesn't appear valid"
        if form['password'] != form['confirm']:
            errors['pass'] = "Passwords don't match"
        if len(form['lname']) > 15 or len(form['fname']) > 15:
            errors['name'] = 'Name fields can have up to 15 characters'
        if len(form['password']) < 8:
            errors['pass'] = 'Password must be at least 8 characters'
        if not valiDate(form['bday']):
            errors['bday'] = 'Birthday field is empty or invalid'
        return errors
    
    def login_validator(self, form):
        errors = {}
        if len(form['email']) < 1:
            errors['email'] = 'Empty field'
        elif len(form['email']) > 1:
            try:
                User.objects.get(email=form['email'])
            except:
                errors['exist'] = "Email is not registered"
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, form):
        errors = {}
        if len(form['quotedBy']) < 3:
            errors['quotedBy'] = "'Quoted By' field must have more than 3 characters"
        if len(form['message']) < 10:
            errors['message'] = "'Message' field must have more than 10 characters"
        return errors

class User(models.Model):
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    bday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "{}: {} {}".format(self.id, self.fname, self.lname)

class Quote(models.Model):
    quoted_by = models.CharField(max_length=30)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name='quotes_uploaded')
    favorited_by = models.ManyToManyField(User, related_name='favorite_quotes')
    objects = QuoteManager()

def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def valiDate(date):
    if date=='':
        return False
    else:
        now = datetime.now()
        print(now)
        print(date)
        if datetime.strptime(date,'%Y-%m-%d') <= now:
            return True
        else:
            return False