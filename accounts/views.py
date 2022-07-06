from time import strftime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from . import forms,models
from django.contrib import messages
from django.contrib.auth.decorators import login_required



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


    return render(request,'accounts/account_management/editPass.html',context)
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
def muleInspectionEntry(request):
    
    if request.method == 'POST':
        newentry = models.muleInspection(reportedBy = request.user,date=request.POST.get('date'),summary =request.POST.get('summary') )
        newentry.save()
        return redirect('dashBoard')
    return render(request,'accounts/reports/muleInspectionEntry.html')

@login_required(login_url='login')
def dashBoard(request):
  
    return render(request,'accounts/reports/dashBoard.html')

@login_required(login_url='login')
def incidentReportEntry(request):
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
        print(dateFrom)
        print(type(dateFrom))
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
                inceToDel.delete()

    return render(request,'accounts/reports/locations.html',{'locations':locationsAll})