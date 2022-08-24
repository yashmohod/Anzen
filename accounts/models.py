from operator import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.



class CustomAccountManager(BaseUserManager):

    def create_superuser(self,email,password, **other_fields):

        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_staff',True)

        return self.create_user(email,password, **other_fields)

    def create_user(self,email,password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email = email, **other_fields)
        user.set_password(password)
        user.save()
        return user




class User(AbstractBaseUser,PermissionsMixin):
    badgeNo = models.IntegerField(null=True)
    firstName = models.CharField(max_length=50,null=True)
    lastName = models.CharField(max_length=50,null=True)
    dob = models.DateField( auto_now=False, auto_now_add=False,null=True)
    collegeId = models.IntegerField(null=True)
    status = models.CharField(default='Active',max_length=50, choices=[('Active','Active'),('Not Active','Not Active')])
    email = models.EmailField( max_length=254, unique=True)
    position = models.CharField(max_length=150,null=True,default="Probationary Member")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    objects= CustomAccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        ret = str(self.firstName)+","+str(self.lastName)
        return ret

class inceident (models.Model):
    inceidentName = models.CharField(max_length=150,null=True)
    def __str__(self):
        return self.inceidentName

class location (models.Model):
    locationName = models.CharField(max_length=150,null=True)
    def __str__(self):
        return self.locationName


class incidentReport (models.Model):
    reportedBy  = models.ForeignKey(User,null=False,on_delete=models.PROTECT)
    inceident = models.CharField(max_length=150,null=False)
    date = models.DateField(auto_now=False, auto_now_add=False,null=False)
    receivedTime = models.TimeField(auto_now=False, auto_now_add=False,)
    enrouteTime = models.TimeField(auto_now=False, auto_now_add=False,)
    arivedTime = models.TimeField(auto_now=False, auto_now_add=False,)
    clearTime = models.TimeField(auto_now=False, auto_now_add=False,)
    location = models.CharField(max_length=150,null=False)
    locationDetail = models.CharField(max_length=150, null=True)

    summary = models.TextField()
    def __str__(self):
        ret = str(self.inceident)+' '+str(self.date)+' '+str(self.location)
        return ret

class referral(models.Model):
    incidentReport = models.ForeignKey(incidentReport,null=False,on_delete=models.PROTECT)
    firstName = models.CharField(max_length=150,null=False)
    middleInitial = models.CharField(max_length=150,null=False)
    ICID = models.CharField(max_length=150,null=False)
    dob = models.DateField(auto_now=False, auto_now_add=False,null=False)
    address = models.TextField()
    phoneNo = models.CharField(max_length=150,null=False)

    def __str__(self):
        ret = str(self.inceident)+' '+str(self.firstName)+','+str(self.middleInitial)
        return ret

class timeCard(models.Model):

    who = models.ForeignKey(User,null=False,on_delete=models.PROTECT)
    start = models.DateTimeField(auto_now=False,null=False)
    end = models.DateTimeField(auto_now=False,null=False)
    duration = models.CharField(max_length=150,null=False)
    submitedDate = models.DateTimeField(auto_now=True,null=False)
    approval =  models.CharField(max_length=150,default="Pending")
    note = models.TextField(null=True) 
    def __str__(self):
        ret = str(self.who)+' '+str(self.submitedDate)
        return ret

class clockedIn(models.Model):

    who = models.ForeignKey(User,null=False,on_delete=models.PROTECT)
    start = models.DateTimeField(auto_now=True,null=False)
    
    def __str__(self):
        ret = str(self.who)+' '+str(self.start)
        return ret
