from datetime import datetime
from pyexpat import model
import re
from urllib.parse import urlencode
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from matplotlib.style import context
from requests import request
from . import forms,models
from django.contrib import messages
# Create your views here.

def userLogin(request):

    if request.method == 'POST' :
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate( request,email=email, password= password)
  
        if user is not None :
            login(request,user)
            return redirect('dashBoard')
        else:
            # write code to tell user login unsccessful
            print("failed")
            
    return render(request, 'accounts/account_management/login.html')

def register(request):
    form = forms.creatUserForm(request.POST)
    context ={'regisForm':form }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("userAccounts")
        else:
            messages.error(request,"Passwords did not match or were two short.")


    return render(request,'accounts/account_management/register.html',context)
def editPass(request,userID):
    curRec = models.User.objects.get(id =userID )
    form = forms.editUserPasword(request.POST,instance= curRec )
    context ={'regisForm':form }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("userAccounts")
        else:
            messages.error(request,"Passwords did not match or were two short.")


    return render(request,'accounts/account_management/editPass.html',context)

def userAccounts(request):
    print(request)
    users = models.User.objects.all()
    context ={'users':users }
    if  request.method == 'POST':
        data = request.POST
        lisst = list(data)
        dat = lisst[1]

        buttonFunc = dat[0]
        userID = dat[1:]
        curRec = models.User.objects.get(id =userID )
        if buttonFunc == '0':

            redirect_url = reverse('editUser', args=[userID,request.get_full_path()])
            # parameters = urlencode(curRec)
            return redirect(redirect_url)
        elif buttonFunc == '1':
            curRec.delete()
        elif buttonFunc == '2':
            curstat =curRec.status
            if curstat == 'Active':
                curRec.status = 'Not Active'
                curRec.save()
            elif curstat == 'Not Active':
                curRec.status = 'Active'
                curRec.save()
            else:
                curRec.status = 'Active'
                curRec.save()
        elif buttonFunc == '3':
            redirect_url = reverse('editPass', args=[userID])
            # parameters = urlencode(curRec)
            return redirect(redirect_url)

    return render(request,'accounts/account_management/userAccounts.html',context)

def editUser(request,userID,backurl):

    curRec = models.User.objects.get(id =userID)
    if request.method == 'POST':
        badgeNo = request.POST.get("badgeNo")
        firstName = request.POST.get("firstName")
        lastName = request.POST.get("lastName")
        dob = request.POST.get("dob")
        collegeId = request.POST.get("collegeId")
        status = request.POST.get("status")
        email = request.POST.get("email")

        curRec.badgeNo = badgeNo
        curRec.firstName = firstName
        curRec.lastName = lastName
        curRec.dob = dob
        curRec.collegeId = collegeId
        curRec.status = status
        curRec.email = email

        curRec.save()
        return redirect('userAccounts')

    return render(request,'accounts/account_management/editUser.html',{'user':curRec, 'backurl':backurl})


def incedentEntry(request):
    inceidents = models.inceident.objects.all()
    if request.method =='POST':
        if'newInceident' in request.POST:
            inceident = request.POST['newInceident']
            models.inceident.objects.create(inceidentName=inceident)
        else:
            data = request.POST
            lisst = list(data)
            dat = lisst[1]
            count=0
            buttonFunc =''
            inceidentId =''
            inceidenteditName =''
            for i in dat:
                if i != ',':
                    if count == 0:
                        buttonFunc=buttonFunc+i
                    elif count == 1:
                        inceidentId = inceidentId+i
                    elif count == 2:
                        inceidenteditName = inceidenteditName+i
                else:
                    count = count +1
            
            print(buttonFunc)
            print(inceidentId)
            print(inceidenteditName)
            if buttonFunc == '0':
                inceToedit = models.inceident.objects.get(id=inceidentId)
                inceToedit.inceidentName = inceidenteditName
                inceToedit.save()
            elif buttonFunc == '1':
                inceToDel = models.inceident.objects.get(id=inceidentId)
                inceToDel.delete()

    return render(request,'accounts/reports/inceidentsEntry.html',{'inceidents':inceidents})


def muleInspectionEntry(request):
    
    if request.method == 'POST':
        newentry = models.muleInspection(reportedBy = request.user,date=request.POST.get('date'),summary =request.POST.get('summary') )
        newentry.save()
        return redirect('dashBoard')
    return render(request,'accounts/reports/muleInspectionEntry.html')

def dashBoard(request):
    if request.method == 'POST':
        print(request.POST.get('dashboardNavigationButton'))
        if request.POST.get('dashboardNavigationButton') == '0':
            return redirect('inceidentReportEntry')
        elif request.POST.get('dashboardNavigationButton') == '1':
            return redirect('muleInspectionEntry')
        elif request.POST.get('dashboardNavigationButton') == '2':
            # redirect('')
            pass
        
    return render(request,'accounts/reports/dashBoard.html')

def inceidentReportEntry(request):
    inceidents=models.inceident.objects.all()
    locations = models.location.objects.all()
    if request.method == 'POST':
        newinceidentReportEntry = models.incidentReport(reportedBy = request.user,
        inceident =request.POST.get('inceident'),
        date =request.POST.get('date'),
        receivedTime =request.POST.get('receivedTime'),
        enrouteTime =request.POST.get('enrouteTime'),
        arivedTime =request.POST.get('arivedTime'), 
        clearTime =request.POST.get('clearTime'),
        location = request.POST.get('location'),
        summary =request.POST.get('summary')
        )
        newinceidentReportEntry.save()
        return redirect('dashBoard')
    return render(request,'accounts/reports/inceidentReportEntry.html',{'inceidents':inceidents,'locations':locations})
    

def viewReports(request):


    return render(request,'accounts/reports/viewReports.html')

def locations(request):
    locationsAll = models.location.objects.all()
    if request.method =='POST':
        if'newlocation' in request.POST:
            location = request.POST['newlocation']
            models.location.objects.create(locationName=location)
        else:
            data = request.POST
            lisst = list(data)
            dat = lisst[1]
            count=0
            buttonFunc =''
            inceidentId =''
            inceidenteditName =''
            for i in dat:
                if i != ',':
                    if count == 0:
                        buttonFunc=buttonFunc+i
                    elif count == 1:
                        inceidentId =  inceidentId+i
                    elif count == 2:
                        inceidenteditName =  inceidenteditName+i
                else:
                    count = count +1
            
            print(buttonFunc)
            print(inceidentId)
            print(inceidenteditName)
            if buttonFunc == '0':
                inceToedit = models.location.objects.get(id=inceidentId)
                inceToedit.locationName = inceidenteditName
                inceToedit.save()
            elif buttonFunc == '1':
                inceToDel = models.location.objects.get(id=inceidentId)
                inceToDel.delete()

    return render(request,'accounts/reports/locations.html',{'locations':locationsAll})