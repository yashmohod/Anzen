from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('',views.home,name='home'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('login/',views.userLogin,name='login'),
    path('register/',views.register,name='register'),
    path('userAccounts/',views.userAccounts,name='userAccounts'),
    path('editUser/<int:userID>?<path:backurl>', views.editUser, name='editUser'),
    path('editPass/<int:userID>/',views.editPass,name='editPass'),
    path('incidentEntry/',views.incidentEntry,name='incidentEntry'),
    path('incidentReportEntry/',views.incidentReportEntry,name='incidentReportEntry'),
    path('incidentReportEdit/<int:entryID>/',views.incidentReportEdit,name='incidentReportEdit'),
    path('dashBoard/',views.dashBoard,name='dashBoard'),
    path('viewReports/',views.viewReports,name='viewReports'),
    path('locations/', views.locations,name='locations' )

]

