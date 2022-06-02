from django.urls import path
from django.urls import re_path as url
from . import views


urlpatterns = [
    path('login/',views.userLogin,name='login'),
    path('register/',views.register,name='register'),
    path('userAccounts/',views.userAccounts,name='userAccounts'),
    path('editUser/<int:userID>?<path:backurl>', views.editUser, name='editUser'),
    path('editPass/<int:userID>/',views.editPass,name='editPass'),
    path('incedentEntry/',views.incedentEntry,name='incedentEntry'),
    path('inceidentReportEntry/',views.inceidentReportEntry,name='inceidentReportEntry'),
    path('muleInspectionEntry/',views.muleInspectionEntry,name='muleInspectionEntry'),
    path('dashBoard/',views.dashBoard,name='dashBoard'),

]

