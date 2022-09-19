
from datetime import datetime

from time import strftime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from . import forms,models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseRedirect





# Create your views here.

def home(request):

    return render(request, 'accounts/public/home.html')

def logout(request):
    logout(request)
    return redirect('home')

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


@login_required(login_url='login')
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

@login_required(login_url='login')
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


    return render(request,'accounts/account_management/editpass.html',context)
@login_required(login_url='login')
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
            return redirect(redirect_url)
        elif buttonFunc == '4':
            curUser = models.User.objects.get(id =userID )
            if curUser.position == "Probationary Member":
                curUser.position = "Junior Member"
                curUser.save()
                message = curUser.firstName+" "+curUser.lastName+" "+"Is Promoted !!!"
                messages.success(request, message)
                return HttpResponseRedirect(reverse("userAccounts"))
            elif curUser.position == "Junior Member":
                curUser.position = "Senior Member"
                curUser.save()
                message = curUser.firstName+" "+curUser.lastName+" "+"Is Promoted !!!"
                messages.success(request, message)
                return HttpResponseRedirect(reverse("userAccounts"))
            elif curUser.position == "Senior Member":
                curUser.position = "Executive Board Member"
                curUser.save()
                message = curUser.firstName+" "+curUser.lastName+" "+"Is Promoted !!!"
                messages.success(request, message)
                return HttpResponseRedirect(reverse("userAccounts"))
            else:
                messages.success(request, "Can not be promoted further! ")
                return HttpResponseRedirect(reverse("userAccounts"))


        elif buttonFunc == '5':
            curUser = models.User.objects.get(id =userID )
            if curUser.position == "Junior Member":
                curUser.position = "Probationary Member"
                curUser.save()
                message = curUser.firstName+" "+curUser.lastName+" "+"Is Deomoted !!!"
                messages.success(request, message)
                return HttpResponseRedirect(reverse("userAccounts"))
            elif curUser.position == "Senior Member":
                curUser.position = "Junior Member"
                curUser.save()
                message = curUser.firstName+" "+curUser.lastName+" "+"Is Deomoted !!!"
                messages.success(request, message)
                return HttpResponseRedirect(reverse("userAccounts"))
            elif curUser.position == "Executive Board Member":
                curUser.position = "Senior Member"
                curUser.save()
                message = curUser.firstName+" "+curUser.lastName+" "+"Is Deomoted !!!"
                messages.success(request, message)
                return HttpResponseRedirect(reverse("userAccounts"))
            else:
                messages.success(request, "Can not be deomoted further! ")
                return HttpResponseRedirect(reverse("userAccounts"))

    return render(request,'accounts/account_management/userAccounts.html',context)
@login_required(login_url='login')
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

@login_required(login_url='login')
def incidentEntry(request):
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


@login_required(login_url='login')
def dashBoard(request):
    CoI = models.clockedIn.objects.all()
    clockedIN =[]
    for c in CoI:
        clockedIN.append(c.who)



    if request.POST.get("ClockButton") == "clockIn":
        CoI = models.clockedIn.objects.all()
        clockedIN =[]
        for c in CoI:
            clockedIN.append(c.who)
        if not( request.user in clockedIN):
            clockin = models.clockedIn.objects.create(who=request.user,start= datetime.strptime(request.POST.get("timeNow").replace("T", " "),"%Y-%m-%d %H:%M"))
            clockin.save()
            CoI = models.clockedIn.objects.all()
            return HttpResponseRedirect(reverse("dashBoard"))

    if request.POST.get("ClockButton") == "clockOut":
        clockInRec = models.clockedIn.objects.get(who = request.user)
        endDT = datetime.strptime(request.POST.get("timeNow").replace("T", " "),"%Y-%m-%d %H:%M")
        # print(type(clockInRec.start))
        # print(endDT)
        pop = endDT-clockInRec.start
        print(round(pop.seconds/3600))
        print(round(pop.seconds/60))
        hr = str(round(pop.seconds/3600)).rjust(2, '0')
        min = str(round(pop.seconds/60)).rjust(2, '0')
        dur = hr+":"+min
        models.timeCard.objects.create(who =request.user, start =clockInRec.start,end = endDT,duration = dur  )
        clockInRec.delete()
        CoI = models.clockedIn.objects.all()
        return HttpResponseRedirect(reverse("dashBoard"))


    return render(request,'accounts/reports/dashBoard.html',{'clockedIN':clockedIN})

@login_required(login_url='login')
def incidentReportEntry(request):
    inceidents=models.inceident.objects.all()
    locations = models.location.objects.all()
    if request.method == 'POST':
        print(request.POST)
        #inceident record
        newinceidentReportEntry = models.incidentReport(reportedBy = request.user,
        inceident =request.POST.get('inceident'),
        date =request.POST.get('date'),
        receivedTime =request.POST.get('receivedTime'),
        enrouteTime =request.POST.get('enrouteTime'),
        arivedTime =request.POST.get('arivedTime'),
        clearTime =request.POST.get('clearTime'),
        location = request.POST.get('location'),
        locationDetail = request.POST.get('locationDetail'),
        summary =request.POST.get('summary')
        )
        newinceidentReportEntry.save()
        #referal record

        if((request.POST.get("referralCount")!='' ) and (request.POST.get("referralCount")!= None ) ):
            referralCount = int(request.POST.get("referralCount"))

            while(referralCount!=0):
                newReferral = models.referral(incidentReport=newinceidentReportEntry,
                firstName = request.POST.get('firstName'+str(referralCount)),
                middleInitial = request.POST.get('middleInitial'+str(referralCount)),
                ICID = request.POST.get('ICID'+str(referralCount)),
                dob = request.POST.get('DOB'+str(referralCount)),
                address = request.POST.get('address'+str(referralCount)),
                phoneNo = request.POST.get('PhoneNo'+str(referralCount)),
                )
                newReferral.save()
                referralCount = referralCount-1
        messages.success(request, 'Report Submited Successfully !!!')
        return HttpResponseRedirect(reverse("dashBoard"))

    return render(request,'accounts/reports/inceidentReportEntry.html',{'inceidents':inceidents,'locations':locations})


@login_required(login_url='login')
def incidentReportEdit(request, entryID):
    inc= models.inceident.objects.all()
    loc = models.location.objects.all()
    incidentReport = models.incidentReport.objects.get(id=entryID)
    inceidents =[]
    locations = []
    for l in loc:
        locations.append(str(l))
    for i in inc:
        inceidents.append(str(i))
    print(request.POST)
    if request.method == "POST":
        incidentReport.reportedBy  = models.User.objects.get(id=request.POST.get("reportedBy"))
        incidentReport.inceident = request.POST.get("inceident")
        incidentReport.date = request.POST.get("date")
        incidentReport.receivedTime = request.POST.get("receivedTime")
        incidentReport.enrouteTime = request.POST.get("enrouteTime")
        incidentReport.arivedTime = request.POST.get("arivedTime")
        incidentReport.clearTime = request.POST.get("clearTime")
        incidentReport.location = request.POST.get("location")
        incidentReport.locationDetail = request.POST.get('locationDetail')
        incidentReport.summary = request.POST.get("summary")
        incidentReport.save()
        return redirect("viewReports")


    return render(request,'accounts/reports/inceidentReportEdiit.html',{'inceidents':inceidents,'locations':locations,'incidentReport':incidentReport})



@login_required(login_url='login')
def viewReports(request):
    locationsAll = models.location.objects.all()
    employees = models.User.objects.filter(status='Active')
    inceidents = models.inceident.objects.all()
    incidentReports=[]
    hiddenVal=[]
    searchall=0
    if request.POST.get('button') == 'all':
        searchall =1

    if request.method == 'POST':
        hiddenVal = {'Location':request.POST.get('Location'),'inceident':request.POST.get('inceident'),'Employee':request.POST.get('Employee'),'dateFrom':request.POST.get('dateFrom'),'dateTo' :request.POST.get('dateTo'),'searchAll' :searchall}
        print(request.POST)
        if request.POST.get('button') == 'reportSearch':
            incidentReports = viewincidentReports(request)

        elif request.POST.get('button') == 'all':
            incidentReports = models.incidentReport.objects.all()
        else:
            if request.POST.get('delete') != None:
                incidentReport = models.incidentReport.objects.get(id=request.POST.get('delete'))
                incidentReport.delete()
                incidentReports = viewincidentReportsFil(request.POST.get('Location'),request.POST.get('inceident'),request.POST.get('Employee'),request.POST.get('dateFrom'),request.POST.get('dateTo'),request.POST.get('searchAll'))
            if  request.POST.get('edit') != None:
                id=request.POST.get('edit')
                redirect_url = reverse('incidentReportEdit', args=[id])
                return redirect(redirect_url)

    return render(request,'accounts/reports/viewReports.html',{'locations':locationsAll,'employees':employees,'inceidents':inceidents,'incidentReports':incidentReports,"hiddenVal":hiddenVal})



def viewReferrals(request):
    referrals = []
    Incidents= models.inceident.objects.all()
    if(request.POST.get('button') == 'all'):
        referrals = models.referral.objects.all()
    elif(request.POST.get('button') == 'referralSearch'):
        #print(request.POST)
        referrals=referralSearch(request)
    else:
        if(request.POST.get('delete') != None):
            referral = models.referral.objects.get(id=request.POST.get('delete'))
            referral.delete()
        if  request.POST.get('edit') != None:
            id=request.POST.get('edit')
            redirect_url = reverse('referralEdit', args=[id])
            return redirect(redirect_url)
        if(request.POST.get('view') != None):
            id=request.POST.get('view')
            redirect_url = reverse('viewReport_R', args=[id])
            return redirect(redirect_url)

    return render(request,'accounts/reports/viewReferrals.html',{'referrals':referrals,'Incidents':Incidents})

def  viewReport_R (request,reportID):
    locationsAll = models.location.objects.all()
    employees = models.User.objects.filter(status='Active')
    inceidents = models.inceident.objects.all()
    incidentReports=[models.incidentReport.objects.get(id=reportID)]
    hiddenVal=[]
    searchall=0
    if request.POST.get('button') == 'all':
        searchall =1

    if request.method == 'POST':
        hiddenVal = {'Location':request.POST.get('Location'),'inceident':request.POST.get('inceident'),'Employee':request.POST.get('Employee'),'dateFrom':request.POST.get('dateFrom'),'dateTo' :request.POST.get('dateTo'),'searchAll' :searchall}
        print(request.POST)
        if request.POST.get('button') == 'reportSearch':
            incidentReports = viewincidentReports(request)

        elif request.POST.get('button') == 'all':
            incidentReports = models.incidentReport.objects.all()
        else:
            if request.POST.get('delete') != None:
                incidentReport = models.incidentReport.objects.get(id=request.POST.get('delete'))
                incidentReport.delete()
                incidentReports = viewincidentReportsFil(request.POST.get('Location'),request.POST.get('inceident'),request.POST.get('Employee'),request.POST.get('dateFrom'),request.POST.get('dateTo'),request.POST.get('searchAll'))
            if  request.POST.get('edit') != None:
                id=request.POST.get('edit')
                redirect_url = reverse('incidentReportEdit', args=[id])
                return redirect(redirect_url)

    return render(request,'accounts/reports/viewReports.html',{'locations':locationsAll,'employees':employees,'inceidents':inceidents,'incidentReports':incidentReports,"hiddenVal":hiddenVal})



def referralSearch(request):
    referrals = models.referral.objects.all()
    count = 4
    if request.POST.get("Incident") != 'null':
        count = count -1
        referrals = referrals.filter(incidentReport__inceident=request.POST.get("Incident"))
    if request.POST.get("firstName")!= '':
        count = count -1
        referrals = referrals.filter(firstName=request.POST.get("firstName"))
    if request.POST.get("ICID")!= '':
        count = count -1
        referrals = referrals.filter(ICID =request.POST.get("ICID") )
    if request.POST.get("DOB")!= '':
        count = count -1
        print(request.POST.get("DOB"))
        referrals = referrals.filter(dob = request.POST.get("DOB"))
    if count == 4:
        referrals =[]
    return referrals

def referralEdit(request,referralId):
    referral = models.referral.objects.get(id=referralId)
    inc= models.inceident.objects.all()
    Incidents =[]
    for i in inc:
        Incidents.append(str(i))

    if(request.POST.get("button") =="edit"):
        referral.firstName = request.POST.get("firstName")
        referral.middleInitial =  request.POST.get("middleInitial")
        referral.ICID =  request.POST.get("ICID")
        referral.dob =  request.POST.get("DOB")
        referral.address =  request.POST.get("address")
        referral.phoneNo =  request.POST.get("PhoneNo")
        referral.save()
        return redirect("viewReferrals")

    return render(request,"accounts/reports/referralsEdit.html",{'referral':referral,'Incidents':Incidents})


def viewincidentReports(request):
    incidentReports = models.incidentReport.objects.all()
    count =5
    if request.POST.get('Location') != 'null':
        count = count-1
        incidentReports = incidentReports.filter(location=request.POST.get('Location'))

    if request.POST.get('inceident') != 'null':
        count = count-1
        incidentReports = incidentReports.filter(inceident=request.POST.get('inceident'))

    if request.POST.get('Employee') != 'null':
        count = count-1
        incidentReports = incidentReports.filter(reportedBy__id=request.POST.get('Employee') )

    if request.POST.get('dateFrom') !='' and request.POST.get('dateTo')!='':
        count = count-1
        incidentReports = incidentReports.filter(date__range=[request.POST.get('dateFrom'),request.POST.get('dateTo')])
    elif request.POST.get('dateFrom') !='':
        count = count-1
        dateFrom = strftime(request.POST.get('dateFrom'))

        incidentReports = incidentReports.filter(date__gte=dateFrom)
    elif request.POST.get('dateTo')!='':
        count = count-1
        dateTo = strftime(request.POST.get('dateTo'))
        incidentReports = incidentReports.filter(date__lte=dateTo)
    if count == 5:
        incidentReports=[]
    return incidentReports

def viewincidentReportsFil(Location,inceident,Employee,DateFrom,DateTo,searchall):
    incidentReports = models.incidentReport.objects.all()
    if searchall ==0:

        count =5
        if Location != 'null':
            count = count-1
            incidentReports = incidentReports.filter(location=Location)

        if inceident != 'null':
            count = count-1
            incidentReports = incidentReports.filter(inceident=inceident)

        if Employee != 'null':
            count = count-1
            incidentReports = incidentReports.filter(reportedBy__id=Employee )

        if DateFrom !='' and DateTo!='':
            count = count-1
            incidentReports = incidentReports.filter(date__range=[DateFrom,DateTo])
        elif DateFrom !='':
            count = count-1
            dateFrom = strftime(DateFrom)
            print(dateFrom)
            print(type(dateFrom))
            incidentReports = incidentReports.filter(date__gte=dateFrom)
        elif DateTo!='':
            count = count-1
            dateTo = strftime(DateTo)
            incidentReports = incidentReports.filter(date__lte=dateTo)
        if count == 5:
            incidentReports=[]
    return incidentReports



@login_required(login_url='login')
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
                messages.success(request, "Location:"+'"'+inceToDel.locationName+'"'+" deleted")
                inceToDel.delete()
                return HttpResponseRedirect(reverse("locations"))

    return render(request,'accounts/reports/locations.html',{'locations':locationsAll})



def timeCard(request):
    employees = models.User.objects.all()
    Memployees =models.User.objects.all()
    searchTCs=models.timeCard.objects.all().filter(approval="Pending")
    MsearchTCs= models.timeCard.objects.all().filter(approval="Pending")
    recentTCs = reversed( models.timeCard.objects.all().filter(who =request.user,approval="Pending"))
    MrecentTCs= reversed( models.timeCard.objects.all().filter(who =request.user,approval="Pending"))
    allTcs = reversed(models.timeCard.objects.all().filter(who =request.user).exclude(approval="Pending"))
    MallTcs= reversed(models.timeCard.objects.all().filter(who =request.user).exclude(approval="Pending"))

    if request.POST.get("button")== "deleteTC":
        tc = models.timeCard.objects.get(id= request.POST.get("tcID"))
        tc.delete()
        messages.success(request, 'Time Card deleted successfully!')
        return HttpResponseRedirect(reverse("timeCard"))


    if request.POST.get("button") == "timeCardSubmision" :
        st = datetime.strptime(request.POST.get("start").replace("T", " "),"%Y-%m-%d %H:%M")
        en = datetime.strptime(request.POST.get("end").replace("T", " "),"%Y-%m-%d %H:%M")
        if st > en :
            messages.success(request, 'Input Error!!!')
            messages.success(request, 'Start Time can not be after End Time!')
            return HttpResponseRedirect(reverse("timeCard"))
        nt = request.POST.get("note")
        pop = en - st
        hr = str(pop.seconds // 3600).rjust(2, '0')
        min = str((pop.seconds // 60) - (int(hr) * 60)).rjust(2, '0')
        dur = hr+":"+min

        for tc in models.timeCard.objects.all().filter(who =request.user):
            if (st > tc.start and st < tc.end) or (en > tc.start and en < tc.end):
                messages.success(request, 'There is a time over Lap!!')
                messages.success(request, 'Check the previous time cards.')
                return HttpResponseRedirect(reverse("timeCard"))

        ntc = models.timeCard.objects.create(who = request.user, start = st,duration=dur, end = en,note = nt )
        ntc.save()
        messages.success(request, 'Time Card Submited!!')
        return HttpResponseRedirect(reverse("timeCard"))

    if request.POST.get("button") == "timeCardEditSubmision":
        st = datetime.strptime(request.POST.get("start").replace("T", " "),"%Y-%m-%d %H:%M")
        en = datetime.strptime(request.POST.get("end").replace("T", " "),"%Y-%m-%d %H:%M")
        if st > en :
            messages.success(request, 'Input Error!!!')
            messages.success(request, 'Start Time can not be after End Time!')
            return HttpResponseRedirect(reverse("timeCard"))
        nt = request.POST.get("note")
        tcid = request.POST.get("TCIDedit")
        pop = en - st
        hr = str(pop.seconds // 3600).rjust(2, '0')
        min = str((pop.seconds // 60) - (int(hr) * 60)).rjust(2, '0')
        dur = hr+":"+min

        for tc in models.timeCard.objects.all().filter(who =request.user):
            if (st > tc.start and st < tc.end) or (en > tc.start and en < tc.end):
                messages.success(request, 'There is a time over Lap!!')
                messages.success(request, 'Check the previous time cards.')
                return HttpResponseRedirect(reverse("timeCard"))

        ntc = models.timeCard.objects.get(id = tcid)
        ntc.start= st
        ntc.end= en
        ntc.duration= dur
        ntc.note= nt
        ntc.save()
        messages.success(request, 'Time Card Edited!!')
        return HttpResponseRedirect(reverse("timeCard"))


    if request.POST.get("button")== "ClearTC":
        tcid = request.POST.get("tcID")
        Rtc = models.timeCard.objects.get(id = tcid)
        Rtc.delete()
        messages.success(request, 'Time Card Cleard!!')
        return HttpResponseRedirect(reverse("timeCard"))

    if request.POST.get("button")== "ApproveTC":
        tcid = request.POST.get("tcID")
        Rtc = models.timeCard.objects.get(id = tcid)
        Rtc.approval = "Approved"
        Rtc.save()
        messages.success(request, 'Time Card Approved!!')
        return HttpResponseRedirect(reverse("timeCard"))

    if request.POST.get("button")== "searchTC":

        empID = request.POST.get("Employee")

        dateFrom = request.POST.get("dateFrom")
        dateTo = request.POST.get("dateTo")
        status = request.POST.get("status")
        print(request.POST)
        searchTCs=models.timeCard.objects.all()
        MsearchTCs=models.timeCard.objects.all()
        if empID != "null":
            searchTCs = searchTCs.filter(who__id =empID )
            MsearchTCs = searchTCs.filter(who__id =empID )

        if status != "null":
            searchTCs = searchTCs.filter(approval =status )
            MsearchTCs = searchTCs.filter(approval =status )

        temp =[]
        if dateFrom !='' and dateTo !='':
            print("here")
            dateFrom = datetime.strptime(dateFrom,"%Y-%m-%d")
            dateTo = datetime.strptime(dateTo,"%Y-%m-%d")
            for searchTC in searchTCs:
                if  (dateFrom >= searchTC.start and dateFrom <= searchTC.end) or (dateTo >= searchTC.start and dateTo <= searchTC.end) :
                    temp.append(searchTC)
            searchTCs=temp
            MsearchTCs = temp
        elif dateFrom !='' :
            print("here2")
            dateFrom = datetime.strptime(dateFrom,"%Y-%m-%d")
            for searchTC in searchTCs:
                if  (dateFrom >= searchTC.start and dateFrom <= searchTC.end) or (dateFrom < searchTC.start) :
                    temp.append(searchTC)
            searchTCs=temp
            MsearchTCs = temp
        elif dateTo !='':
            print("here3")
            dateTo = datetime.strptime(dateTo,"%Y-%m-%d")
            for searchTC in searchTCs:
                if  (dateTo <= searchTC.end) or (dateTo >= searchTC.start and dateTo <= searchTC.end) :
                    temp.append(searchTC)
            searchTCs=temp
            MsearchTCs = temp

        return render(request,'accounts/account_management/timeCard.html',{'recentTCs':recentTCs,'allTcs':allTcs, 'employees':employees,'searchTCs':searchTCs,'MrecentTCs':MrecentTCs,'MallTcs':MallTcs, 'Memployees':Memployees,'MsearchTCs':MsearchTCs})

    return render(request,'accounts/account_management/timeCard.html',{'recentTCs':recentTCs,'allTcs':allTcs, 'employees':employees,'searchTCs':searchTCs,'MrecentTCs':MrecentTCs,'MallTcs':MallTcs, 'Memployees':Memployees,'MsearchTCs':MsearchTCs})