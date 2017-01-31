from django.shortcuts import render, redirect
from django.contrib import messages, auth
from datetime import datetime

from ..LogReg.models import User
from .models import Trip, TravelPlan
from dateutil.parser import *


def index(request):
    user = User.objects.get(id = request.session['logged_in_user'])
    y = TravelPlan.objects.filter(travelers=user).values('trips__id')


    context = {
        'user': user,
        "travels": TravelPlan.objects.filter(travelers=user),
        "otherusers": TravelPlan.objects.all().exclude(trips__id__in=y),
    }
    return render(request, "exam/index.html", context)

def logout(request):
    auth.logout(request)
    return redirect("/main")


def add(request):

    return render(request, "exam/add.html")


def newtrip(request):

    # postData = {
    #     "destination": request.POST['destination'],
    #     "description": request.POST['description'],
    #     "startdate": request.POST['startdate'],
    #     "enddate": request.POST['enddate'],
    #     "user_id": request.session['logged_in_user'],
    # }
    #
    # user = User.objects.get(id=request.session['logged_in_user'])
    # result = Trip.objects.tripValidate(postData)
    #
    # if result[0]:
    #     for error in result[1]
    #         messages.error(request, error)
    #
    # else:
    #     TravelPlan.objects.create(trips=result[1], travelers=user)
    #


    errors=[]
    flag = False
    if not request.POST['destination']:
        errors.append("Destination is blank.")
        flag = True
    if not request.POST['startdate']:
        errors.append("Start date is blank.")
        flag = True
    if not request.POST['enddate']:
        errors.append("End date is blank.")
        flag = True
    if flag:
        for err in errors:
            messages.error(request, err)
        return redirect("/travels/add")

    startdate = datetime.strptime(request.POST['startdate'], "%Y-%m-%d")
    enddate = datetime.strptime(request.POST['enddate'],"%Y-%m-%d")
    user = User.objects.get(id=request.session['logged_in_user'])

    if datetime.now() > startdate:
        messages.error(request, "Start date should be today or after today's date.")
        return redirect("/travels/add")
    if startdate > enddate:
        messages.error(request, "Start date must be before End date.")
        return redirect("/travels/add")

    trip = Trip.objects.create(
        destination=request.POST['destination'],
        description=request.POST['description'],
        startdate=startdate,
        enddate=enddate,
        owner=user,
    )

    TravelPlan.objects.create(trips=trip, travelers=user)


    return redirect("/travels")


def join(request, id):
    trip = Trip.objects.get(id=id)
    user = User.objects.get(id = request.session['logged_in_user'])

    TravelPlan.objects.create(trips=trip, travelers=user)

    return redirect("/travels")


def destination(request, id):
    user = User.objects.get(id = request.session['logged_in_user'])
    trip = Trip.objects.get(id=id)


    travels = Trip.objects.filter(id=id)
    others = TravelPlan.objects.filter(trips=trip).exclude(travelers=user).exclude(travelers=trip.owner)

    context={
        "travels": travels,
        "others": others,
    }
    return render(request, 'exam/destination.html', context)


def edit(request,id):

    context = {
        "trip": Trip.objects.get(id=id),
    }

    return render(request, "exam/edit.html", context)

def edited(request,id):
    editedTrip = Trip.objects.get(id=id)
    editedTrip.destination = request.POST['destination']
    editedTrip.description = request.POST['description']
    editedTrip.startdate = datetime.strptime(request.POST['startdate'], "%Y-%m-%d")
    editedTrip.enddate = datetime.strptime(request.POST['enddate'], "%Y-%m-%d")
    editedTrip.save()

    return redirect("/travels")


def delete(request, id):
    Trip.objects.get(id=id).delete()

    return redirect("/travels")
