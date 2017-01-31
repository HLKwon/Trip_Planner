from __future__ import unicode_literals
from django.db import models
import re, bcrypt



lettersOnly = re.compile(r'^[a-zA-Z]*$')
# emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class userManager(models.Manager):
    def rValidate(self, postData):
        errors = []
        flag = False

        if not postData['name']:
            errors.append('Name must not be blank.')
            flag = True
        if len(postData['name']) < 2:
            errors.append('Name must be longer than 2 characters.')
            flag = True
        if not lettersOnly.match(postData['name']):
            errors.append('Name must not contain numbers.')
            flag = True

        # if not postData['lname']:
        #     errors.append('Last name must not be blank.')
        #     flag = True
        # if len(postData['lname']) < 2:
        #     errors.append('Last name must be longer than 2 characters.')
        #     flag = True
        # if not lettersOnly.match(postData['lname']):
        #     errors.append('Last name must not contain numbers.')
        #     flag = True

        if not postData['username']:
            errors.append('Username must not be blank.')
            flag = True
        if len(postData['username']) < 2:
            errors.append('Username must be longer than 2 characters.')
            flag = True
        # if not emailRegex.match(postData['username']):
        #     errors.append('Username must be valid.')
        #     flag = True

        if not postData['password']:
            errors.append('Password must not be blank')
            flag = True
        if len(postData['password']) < 8:
            errors.append('Password must be greater than 8 characters')
            flag = True
        if postData['password'] != postData['cPassword']:
            errors.append('Passwords must match!')
            flag = True

        if not flag:
            hashedPW = bcrypt.hashpw( postData['password'].encode(), bcrypt.gensalt() )
            user = User.objects.create(
                name=postData['name'],
                username=postData['username'],
                password=hashedPW,
            )
            return(flag, user)

        return (flag, errors)


    def lValidate(self, postData):

        if not postData['password']:
            return(False, "Login credentials are invalid.")

        user = User.objects.get(username=postData['username'])
        password = postData['password'].encode()
        hashed = user.password.encode()

        if bcrypt.hashpw(password, hashed) == hashed:
            return (True, user)

        return(False, "Login credentials are invalid.")





class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()
