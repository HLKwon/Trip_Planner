from __future__ import unicode_literals

from django.db import models

from ..LogReg.models import User

from dateutil.parser import *
from datetime import *

# Create your models here.

class tripManager(models.Manager):
    def tripValidate(self, postData):
        errors=[]
        flag = False

        if not postData['destination']:
            errors.append('Name must not be blank.')
            flag=True
        if not postData['startdate']:
            errors.append('Start date must not be blank.')
            flag=True
        if not postData['enddate']:
            errors.append('End date must not be blank.')
            flag=True
        if flag:
            return (flag, errors)


        startdate = parse(postData['startdate'])
        enddate = parse(postData['enddate'])
        


        user = User.objects.get(id=user_id)

        if startdate > enddate:
            errors.append('Start date can not be after end date.')
            flag=True
            return (flag, errors)

        if not flag:
            trip=Trip.objects.create(
                destination=postData['destination'],
                description=postData['description'],
                startdate=startdate,
                enddate=enddate
            )

        return (False, trip)



class Trip(models.Model):
    destination = models.CharField(max_length = 45)
    description = models.TextField(max_length = 1000)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    owner = models.ForeignKey("LogReg.User")
    created_at = models.DateTimeField(auto_now_add = True)
    objects = tripManager()

class TravelPlan(models.Model):
    trips = models.ForeignKey('Trip', related_name="trips")
    travelers = models.ForeignKey('LogReg.User', related_name="travelers")
