from django.contrib import admin
from django.urls import path, include
from dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('addstd/', views.addstd, name='addstd'),
    path('delstd/', views.delstd, name='delstd'),
    path('addprt/', views.addprt, name='addprt'),
    path('delprt/', views.delprt, name='delprt'),
    path('markatten/', views.markatten, name='markatten'),
    path('events/', views.events, name='events'),


    #For registrations and logout
    path('parentreg', views.handleparentreg, name='handleparentreg'),
    path('studentreg', views.handlestudentreg, name='handlestudentreg'),
    path('logout/', views.handlelogout, name='handlelogout'),


    # #For Classes
    # path('class-1/', views.classOne, name='classOne'),
    # path('class-2/', views.classTwo, name='classTwo'),
    # path('class-3/', views.classThree, name='classThree'),
    # path('class-4/', views.classFour, name='classFour'),
    # path('class-5/', views.classFive, name='classFive'),
    # path('class-6/', views.classSix, name='classSix'),
    # path('class-7/', views.classSeven, name='classSeven'),
    # path('class-8/', views.classEight, name='classEight'),
    # path('class-9/', views.classNine, name='classNine'),
    # path('class-10/', views.classTen, name='classTen'),


    #for deleting parents from database
    path('delprtid/<str:Email>', views.deleteparent, name='deleteparent'),
    #for deleting students from database
    path('delstdid/<int:Id>', views.deletestudent, name='deletestudent'),


    #for attendence page
    path('attendence/<int:Id>', views.attendence, name='attendence'),
    #for uploading attendence
    path('uploadattendence', views.uploadattendence, name='uploadattendence'),
    #for deleting attendence
    path('deleteattendence/<int:Id>', views.deleteattendence, name='deleteattendence'),


    #for result page
    path('result/<int:Id>', views.result, name='result'),
    #for uploading results
    path('uploadresults', views.uploadresults, name='uploadresults'),
    #for saving results
    path('saveresult', views.saveresult, name='saveresult'),
    #for deleting result
    path('deleteresult/<int:Id>', views.deleteresult, name='deleteresult'),


    #for event form
    path('events/uploadevent', views.uploadevent, name='uploadevent'),
    # for deleting events
    path('deleteevent/<int:Id>', views.deleteevent, name='deleteevent'),



    #for adding a class to db
    path('addclass', views.addclass, name='addclass'),
    #To redirect to class details
    path('class/<int:Id>', views.classdetails, name='classdetails'),
    #for deleting a class from db
    path('deleteclass/<int:Id>', views.deleteclass, name='deleteclass'),



    #for uploading a test
    path('uploadtest', views.uploadtest, name='uploadtest'),
    #for saving a test in db
    path('savetest', views.savetest, name='savetest'),
    #for Upcoming tests page
    path('upcoming-tests/<int:Id>', views.upcomingtest, name='upcomingtest'),
    #for deleting upcomingtest
    path('deletetest/<int:Id>', views.deletetest, name='deletetest'),


]