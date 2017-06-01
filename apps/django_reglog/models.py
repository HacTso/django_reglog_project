from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
NAME_REGEX =re.compile('^[A-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def register(self, postData):
    	errors = []
    	#check if email exists
    	if User.objects.filter(email=postData['email']):
    		errors.append('Email is already registered')
    	# validate username
    	if len(postData['username']) < 2:
    		errors.append('Username must be at least 2 characters')
    	elif not NAME_REGEX.match(postData['username']):
    		errors.append('Username must only contain alphabet')
    	# validate email
    	if len(postData['email']) < 1:
    		errors.append('Email cannot be blank')
    	elif not EMAIL_REGEX.match(postData['email']):
    		errros.append('Invaild email format')
    	# validate password
    	if len(postData['password']) < 8:
    		errors.append('Password must be at least 8 characters')
    	# validate confirm passowrd
    	elif postData['password'] != postData['confirm']:
    		errors.append('Password do not match')
    	
    	# if no errors
    	if len(errors) == 0:
    		# hash pw with password(encode) and (gen)salt
    		reg_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
    		# add to database
    		User.objects.create(username=postData['username'], email=postData['email'], password=reg_pw)

    	return errors

    def login(self, postData):
        errors = []
        # if email is found in db
        if User.objects.filter(email=postData['email']):
            db_pw = User.objects.get(email=postData['email']).password
            print db_pw
            login_pw = bcrypt.hashpw(postData['password'].encode(), db_pw.encode())
            print login_pw
            # check if passwords not match, then flash messages
            if not login_pw == db_pw:
                errors.append('Incorrect password')
        #else if email is not found in db
        else:
            errors.append('Email has not been registered')

        return errors

class User(models.Model):
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return str(self.id) + self.username + self.email + self.password
   














