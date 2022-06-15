from pyclbr import Class
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from account.models import Account
from dashboard.models import Attendence_Report, Event, Parent, Result_Card, Student, Class, Upcoming_Test
from django.contrib.auth import logout
from django.contrib import messages


# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_school:
            classes = Class.objects.filter(school=request.user.school).order_by('class_no')
        if request.user.is_parent:
            classes = Class.objects.filter(school=request.user.parent.school).order_by('class_no')
        return render(request, 'dashboard/dashboard.html', {'classes' : classes})
    else:
        return redirect('notfound')
    

def addstd(request):
    if request.user.is_authenticated and request.user.is_school:
        return render(request, 'dashboard/addstd.html')
    else:
        return redirect('notfound')

def delstd(request):
    if request.user.is_authenticated and request.user.is_school:
        studentdata = Student.objects.filter(school=request.user.school)
        return render(request, 'dashboard/delstd.html', {'studentdata' : studentdata})
    else:
        return redirect('notfound')
    

def addprt(request):
    if request.user.is_authenticated and request.user.is_school:
        return render(request, 'dashboard/addprt.html')
    else:
        return redirect('notfound')
    

def delprt(request):
    if request.user.is_authenticated and request.user.is_school:
        parentdata = Parent.objects.filter(school=request.user.school)
        return render(request, 'dashboard/delprt.html', {'parentdata' : parentdata})
    else:
        return redirect('notfound')
    

def markatten(request):
    if request.user.is_authenticated and request.user.is_school:
        return render(request, 'dashboard/markatten.html')
    else:
        return redirect('notfound')

    
def events(request):
    if request.user.is_authenticated:
        if request.user.is_school:
            school = request.user.school
        if request.user.is_parent:
            school = request.user.parent.school
        events = Event.objects.filter(school=school).order_by('-id')
        return render(request, 'dashboard/events.html', {'events' : events})
    else:
        return redirect('notfound')
    





#For registrations and logout
def handleparentreg(request):
    if request.method=="POST":
        # get the post parameters
        username = request.POST['pname'] 
        address = request.POST['address'] 
        contact = request.POST['contact'] 
        cnic = request.POST['cnic'] 
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #checks for errors
        if not address.isalnum():
            messages.warning(request, 'Address must only contain alphabets or numbers!')
            return redirect('/dashboard/addprt')

        if not len(cnic) == 13:
            messages.warning(request, 'Invalid CNIC number')
            return redirect('/dashboard/addprt')

        if Parent.objects.filter(cnic=cnic).exists():
            messages.warning(request, 'CNIC number already exists!')
            return redirect('/dashboard/addprt')

        if Account.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists!')
            return redirect('/dashboard/addprt')

        if len(pass1) < 6:
            messages.warning(request, 'Password must contain atleast 6 characters')
            return redirect('/dashboard/addprt')

        if pass1 != pass2:
            messages.error('password do not match')
            return redirect('/dashboard/addprt')  
        
        #adding data to accounts table
        myuser = Account.objects.create_user(email, username, pass1)
        myuser.is_parent = True
        myuser.save()

        #adding data to Parents table
        account = myuser
        school = request.user.school
        myparent = Parent(parent_name=username, address=address, contact=contact, cnic=cnic, email=email, school=school, account=account)
        myparent.save()
        
        if Student.objects.filter(father_cnic=cnic).exists():
            student      = Student.objects.get(father_cnic=cnic)
            student.parent = myparent
            student.save()


        messages.success(request, "Parent has been added successfully")
        return redirect('/dashboard/addprt')


    else:
        return redirect('notfound')





def handlestudentreg(request):
    if request.method=="POST":
        # get the post parameters
        studentname     = request.POST['name'] 
        studentclass    = request.POST['class'] 
        rollnum         = request.POST['rollnum'] 
        gender          = request.POST['gender']
        dob             = request.POST['dob']
        age             = request.POST['age']
        fathercnic      = request.POST['fathercnic'] 

        school          = request.user.school

        #checks for errors
        if not studentname.isalpha():
            messages.warning(request, 'Invalid student name')
            return redirect('/dashboard/addstd')

        if not studentclass.isnumeric():
            messages.warning(request, 'Invalid class')
            return redirect('/dashboard/addstd')


        if not Class.objects.filter(class_no=studentclass, school=request.user.school).exists():
            messages.warning(request, 'The class does not exists. please create the class first')
            return redirect('/dashboard/addstd')


        if gender != 'Male' and gender != 'Female' and gender != 'Others':
            messages.warning(request, 'Invalid gender')
            return redirect('/dashboard/addstd')

        if not len(fathercnic) == 13:
            messages.warning(request, 'Invalid CNIC number')
            return redirect('/dashboard/addstd')

        classno    = Class.objects.get(class_no=studentclass, school=school)


  
        #adding data to Student table
        mystudent       = Student(name=studentname, roll_number=rollnum, gender=gender,
         dob=dob, age=age, father_cnic=fathercnic, school=school, student_class=classno)
        mystudent.save()
        
        if Parent.objects.filter(cnic=fathercnic).exists():
            parent      = Parent.objects.get(cnic=fathercnic)
            mystudent.parent   = parent
            mystudent.save()


        messages.success(request, "Student has been added successfully")
        return redirect('/dashboard/addstd')


    else:
        return redirect('notfound')
        

def handlelogout(request):
    logout(request)
    messages.success(request, 'logged Out Successfully')
    return redirect('/')




# #For Classes
# def classOne(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=1).order_by('roll_number')
#         if request.user.is_parent:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=1).order_by('roll_number')
#         return render(request, 'dashboard/classes/class1.html', {'studentdata' : studentdata})

#     else:
#         return redirect('notfound')

# def classTwo(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=2).order_by('roll_number')
#         if request.user.is_parent:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=2).order_by('roll_number')
#         return render(request, 'dashboard/classes/class2.html', {'studentdata' : studentdata})

#     else:
#         return redirect('notfound') 
    

# def classThree(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=3).order_by('roll_number')
#         if request.user.is_parent:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=3).order_by('roll_number')
#         return render(request, 'dashboard/classes/class3.html', {'studentdata' : studentdata})

#     else:
#         return redirect('notfound') 

# def classFour(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=4).order_by('roll_number')
#         if request.user.is_parent:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=4).order_by('roll_number')
#         return render(request, 'dashboard/classes/class4.html', {'studentdata' : studentdata})
#     else:
#         return redirect('notfound')

# def classFive(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=5).order_by('roll_number')
#         if request.user.is_parent:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=5).order_by('roll_number')
#         return render(request, 'dashboard/classes/class5.html', {'studentdata' : studentdata})
#     else:
#         return redirect('notfound')

# def classSix(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=6).order_by('roll_number')
#         if request.user.is_parent:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=6).order_by('roll_number')
#         return render(request, 'dashboard/classes/class6.html', {'studentdata' : studentdata})
#     else:
#         return redirect('notfound')

# def classSeven(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=7).order_by('roll_number')
#         if request.user.is_parent:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=7).order_by('roll_number')
#         return render(request, 'dashboard/classes/class7.html', {'studentdata' : studentdata})
#     else:
#         return redirect('notfound')

# def classEight(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=8).order_by('roll_number')
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=8).order_by('roll_number')
#         return render(request, 'dashboard/classes/class8.html', {'studentdata' : studentdata})
#     else:
#         return redirect('notfound')

# def classNine(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=9).order_by('roll_number')
#         if request.user.is_parent:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=9).order_by('roll_number')
#         return render(request, 'dashboard/classes/class9.html', {'studentdata' : studentdata})
#     else:
#         return redirect('notfound')

# def classTen(request):
#     if request.user.is_authenticated:
#         if request.user.is_school:
#             studentdata = Student.objects.filter(school=request.user.school, student_class=10).order_by('roll_number')
#         if request.user.is_parent:
#             studentdata = Student.objects.filter(school=request.user.parent.school, student_class=10).order_by('roll_number')
#         return render(request, 'dashboard/classes/class10.html', {'studentdata' : studentdata})
#     else:
#         return redirect('notfound')


#for deleting parents from database
def deletestudent(request, Id):
    student = Student.objects.filter(id=Id)
    student.delete()
    messages.success(request, "Student has been deleted successfully")
    return redirect('/dashboard/delstd')
    


#for deleting parents from database
def deleteparent(request, Email):
    parent = Parent.objects.filter(email=Email)
    account = Account.objects.filter(email=Email)
    parent.delete()
    account.delete()
    messages.success(request, "Parent has been deleted successfully")
    return redirect('/dashboard/delprt')





#for uploading attendence to database
def uploadattendence(request):
    if request.method == "POST":
        monday = request.POST.get('monday') == 'true'
        tuesday = request.POST.get('tuesday') == 'true'
        wednesday = request.POST.get('wednesday') == 'true'
        thursday = request.POST.get('thursday') == 'true'
        friday = request.POST.get('friday') == 'true'
        saturday = request.POST.get('saturday') == 'true'

        if monday == True:
            monday = "Present"
        else:
            monday = "Absent"
        if tuesday == True:
            tuesday = "Present"
        else:
            tuesday = "Absent"
        if wednesday == True:
            wednesday = "Present"
        else:
            wednesday = "Absent"
        if thursday == True:
            thursday = "Present"
        else:
            thursday = "Absent"
        if friday == True:
            friday = "Present"
        else:
            friday = "Absent"
        if saturday == True:
            saturday = "Present"
        else:
            saturday = "Absent"

        
        studentclass = request.POST['class']
        studentrollnum = request.POST['rollnum']

        #checks for errors
        if not Student.objects.filter(roll_number=studentrollnum, student_class=studentclass).exists():
            messages.warning(request, 'No such student exists')
            return redirect('/dashboard/markatten')

        if studentclass != 1 and studentclass != 2 and studentclass != 3 and studentclass != 4 and studentclass != 5 and studentclass != 6 and studentclass != 7 and studentclass != 8 and studentclass != 9 and studentclass != 10:
            messages.warning(request, 'Class does not exists')
            return redirect('/dashboard/markatten')


        student = Student.objects.get(student_class=studentclass, roll_number=studentrollnum)

        myattendence = Attendence_Report(Monday=monday, Tuesday=tuesday, Wednesday=wednesday, Thursday=thursday, Friday=friday, Saturday=saturday, student=student)
        myattendence.save()

        messages.success(request, "Attendence has been uploaded successfully")

        return redirect('/dashboard/markatten')



#for attendence
def attendence(request, Id):
    if request.user.is_authenticated:
        mystudent = Student.objects.get(id=Id)
        attendence = Attendence_Report.objects.filter(student=mystudent)
        return render(request, 'dashboard/attendence.html', {'attendence' : attendence, 'student' : mystudent})
    else:
        return redirect('notfound')


#for deleting attendence
def deleteattendence(request, Id):
    attendence = Attendence_Report.objects.get(id=Id)
    student = attendence.student
    student = student.id
    attendence.delete()
    messages.success(request, "Attendence has been deleted successfully")
    return redirect('attendence', student)    

#for result
def result(request, Id):
    if request.user.is_authenticated:
        mystudent = Student.objects.get(id=Id)
        results = Result_Card.objects.filter(student=mystudent).order_by('-id')
        return render(request, 'dashboard/result.html', {'results' : results, 'student' : mystudent})
    else:
        return redirect('notfound')

#for uploading results
def uploadresults(request):
    if request.user.is_authenticated and request.user.is_school:
        return render(request, 'dashboard/uploadresults.html')
    else:
        return redirect('notfound')

#for saving results in db
def saveresult(request):
    if request.method == 'POST':
        studentrollnum             = request.POST['rollnum']
        studentclass               = request.POST['class']

        urduobtained               = request.POST['urduobtained']
        urdutotal                  = request.POST['urdutotal']
        englishobtained            = request.POST['englishobtained']
        englishtotal               = request.POST['englishtotal']
        mathsobtained              = request.POST['mathsobtained']
        mathstotal                 = request.POST['mathstotal']
        physicsobtained            = request.POST['physicsobtained']
        physicstotal               = request.POST['physicstotal']
        chemistryobtained          = request.POST['chemistryobtained']
        chemistrytotal             = request.POST['chemistrytotal']
        bioobtained                = request.POST['bioobtained']
        biototal                   = request.POST['biototal']
        computerobtained           = request.POST['computerobtained']
        computertotal              = request.POST['computertotal']
        pakstudiesobtained         = request.POST['pakstudiesobtained']
        pakstudiestotal            = request.POST['pakstudiestotal']
        scienceobtained            = request.POST['scienceobtained']
        sciencetotal               = request.POST['sciencetotal']
        islamiyatobtained          = request.POST['islamiyatobtained']
        islamiyattotal             = request.POST['islamiyattotal']
        arabicobtained             = request.POST['arabicobtained']
        arabictotal                = request.POST['arabictotal']
        totalobtained              = request.POST['totalobtained']
        grandtotal                 = request.POST['grandtotal']

        if urduobtained == "":
            urduobtained=None
        if urdutotal == "":
            urdutotal=None
        if englishobtained == "":
            englishobtained=None
        if englishtotal == "":
            englishtotal=None
        if mathsobtained == "":
            mathsobtained=None
        if mathstotal == "":
            mathstotal=None
        if physicsobtained == "":
            physicsobtained=None
        if physicstotal == "":
            physicstotal=None
        if chemistryobtained == "":
            chemistryobtained=None
        if chemistrytotal == "":
            chemistrytotal=None
        if bioobtained == "":
            bioobtained=None
        if biototal == "":
            biototal=None
        if computerobtained == "":
            computerobtained=None
        if computertotal == "":
            computertotal=None
        if pakstudiesobtained == "":
            pakstudiesobtained=None
        if pakstudiestotal == "":
            pakstudiestotal=None
        if scienceobtained == "":
            scienceobtained=None
        if sciencetotal == "":
            sciencetotal=None
        if islamiyatobtained == "":
            islamiyatobtained=None
        if islamiyattotal == "":
            islamiyattotal=None
        if arabicobtained == "":
            arabicobtained=None
        if arabictotal == "":
            arabictotal=None
        if totalobtained == "":
            totalobtained=None
        if grandtotal == "":
            grandtotal=None

        #checks for errors
        if not Student.objects.filter(roll_number=studentrollnum, student_class=studentclass).exists():
            messages.warning(request, 'No such student exists')
            return redirect('/dashboard/uploadresults')

        if not urduobtained == None:
            if int(urduobtained) >= 0 and urdutotal == None:
                messages.warning(request, 'Invalid input at Urdu')
                return redirect('/dashboard/uploadresults')

            if int(urduobtained) > int(urdutotal):
                messages.warning(request, 'Invalid input at Urdu')
                return redirect('/dashboard/uploadresults')

        if not englishobtained == None:
            if int(englishobtained) >= 0 and englishtotal == None:
                messages.warning(request, 'Invalid input at English')
                return redirect('/dashboard/uploadresults')

            if int(englishobtained) > int(englishtotal):
                messages.warning(request, 'Invalid input at English')
                return redirect('/dashboard/uploadresults')

        if not mathsobtained == None:
            if int(mathsobtained) >= 0 and mathstotal == None:
                messages.warning(request, 'Invalid input at Mathematics')
                return redirect('/dashboard/uploadresults')

            if int(mathsobtained) > int(mathstotal):
                messages.warning(request, 'Invalid input at Mathematics')
                return redirect('/dashboard/uploadresults')

        if not physicsobtained == None:
            if int(physicsobtained) >= 0 and physicstotal == None:
                messages.warning(request, 'Invalid input at Physics')
                return redirect('/dashboard/uploadresults')

            if int(physicsobtained) > int(physicstotal):
                messages.warning(request, 'Invalid input at Physics')
                return redirect('/dashboard/uploadresults')

        if not chemistryobtained == None:
            if int(chemistryobtained) >= 0 and chemistrytotal == None:
                messages.warning(request, 'Invalid input at Chemistry')
                return redirect('/dashboard/uploadresults')

            if int(chemistryobtained) > int(chemistrytotal):
                messages.warning(request, 'Invalid input at Chemistry')
                return redirect('/dashboard/uploadresults')

        if not bioobtained == None:
            if int(bioobtained) >= 0 and biototal == None:
                messages.warning(request, 'Invalid input at Bio')
                return redirect('/dashboard/uploadresults')

            if int(bioobtained) > int(biototal):
                messages.warning(request, 'Invalid input at Bio')
                return redirect('/dashboard/uploadresults')

        if not computerobtained == None:
            if int(computerobtained) >= 0 and computertotal == None:
                messages.warning(request, 'Invalid input at Computer')
                return redirect('/dashboard/uploadresults')

            if int(computerobtained) > int(computertotal):
                messages.warning(request, 'Invalid input at Computer')
                return redirect('/dashboard/uploadresults')

        if not pakstudiesobtained == None:
            if int(pakstudiesobtained) >= 0 and pakstudiestotal == None:
                messages.warning(request, 'Invalid input at Pak-Studies')
                return redirect('/dashboard/uploadresults')

            if int(pakstudiesobtained) > int(pakstudiestotal):
                messages.warning(request, 'Invalid input at Pak-Studies')
                return redirect('/dashboard/uploadresults')

        if not scienceobtained == None:
            if int(scienceobtained) >= 0 and sciencetotal == None:
                messages.warning(request, 'Invalid input at Science')
                return redirect('/dashboard/uploadresults')

            if int(scienceobtained) > int(sciencetotal):
                messages.warning(request, 'Invalid input at Science')
                return redirect('/dashboard/uploadresults')

        if not islamiyatobtained == None:
            if int(islamiyatobtained) >= 0 and islamiyattotal == None:
                messages.warning(request, 'Invalid input at Islamiyat')
                return redirect('/dashboard/uploadresults')

            if int(islamiyatobtained) > int(islamiyattotal):
                messages.warning(request, 'Invalid input at Islamiyat')
                return redirect('/dashboard/uploadresults')

        if not arabicobtained == None:
            if int(arabicobtained) >= 0 and arabictotal == None:
                messages.warning(request, 'Invalid input at Arabic')
                return redirect('/dashboard/uploadresults')

            if int(arabicobtained) > int(arabictotal):
                messages.warning(request, 'Invalid input at Arabic')
                return redirect('/dashboard/uploadresults')

        if not totalobtained == None:
            if int(totalobtained) >= 0 and grandtotal == None:
                messages.warning(request, 'Invalid input at Total')
                return redirect('/dashboard/uploadresults')

            if int(totalobtained) > int(grandtotal):
                messages.warning(request, 'Invalid input at Total')
                return redirect('/dashboard/uploadresults')

        

        student = Student.objects.get(student_class=studentclass, roll_number=studentrollnum)

        myresult = Result_Card(urdu_obtained=urduobtained, urdu_total=urdutotal, english_obtained=englishobtained, english_total=englishtotal,
        maths_obtained=mathsobtained, maths_total=mathstotal, physics_obtained=physicsobtained, physics_total=physicstotal,
        chemistry_obtained=chemistryobtained, chemistry_total=chemistrytotal, bio_obtained=bioobtained, bio_total=biototal,
        computer_obtained=computerobtained, computer_total=computertotal, pakstudies_obtained=pakstudiesobtained, pakstudies_total=pakstudiestotal,
        islamiyat_obtained=islamiyatobtained, islamiyat_total=islamiyattotal, science_obtained=scienceobtained, science_total=sciencetotal,
        arabic_obtained=arabicobtained, arabic_total=arabictotal, total_obtained=totalobtained, total_marks=grandtotal, student=student)
        myresult.save()

        messages.success(request, "Result has been uploaded successfully")

        return redirect('/dashboard/uploadresults')



#for deleting result
def deleteresult(request, Id):
    result = Result_Card.objects.get(id=Id)
    student = result.student
    student = student.id
    result.delete()
    messages.success(request, "Result has been deleted successfully")
    return redirect('result', student)    



#for event uploading
def uploadevent(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]

        #checks for errors
        if not title.isalnum():
            messages.warning(request, 'Invalid title')
            return redirect('/dashboard/events')

        school = request.user.school

        myevent = Event(title=title, description=description, school=school)
        myevent.save()

        messages.success(request, "Event has been uploaded successfully")
    return redirect('/dashboard/events')


#for deleting event
def deleteevent(request, Id):
    event = Event.objects.get(id=Id)
    event.delete()
    messages.success(request, "Event has been deleted successfully")
    return redirect('/dashboard/events')


def addclass(request):
    if request.method == 'POST':
        classtitle          = request.POST['title']
        classno             = request.POST['class']
        school              = request.user.school

        myclass             = Class(class_no = classno, class_title=classtitle, school=school)
        myclass.save()

        messages.success(request, "Class has been created successfully")
        return redirect('dashboard')


def classdetails(request, Id):
    if request.user.is_authenticated:
        studentclass    = Class.objects.get(id=Id)
        students        = Student.objects.filter(student_class=studentclass).order_by('roll_number')
        classdetails    = Id
        return render(request, 'dashboard/class.html', {'students':students, 'classid':Id})
    else:
        return redirect('notfound')

def deleteclass(request, Id):
    if request.user.is_authenticated and request.user.is_school:
        myclass = Class.objects.get(id=Id)
        myclass.delete()
        messages.success(request, "Class has been deleted successfully")
        return redirect('/dashboard')

    else:
        return redirect('notfound')


def uploadtest(request):
    return render(request, 'dashboard/uploadtest.html')


def savetest(request):
    if request.user.is_authenticated and request.user.is_school:
        if request.method == 'POST':
            forclass           = request.POST['class']
            subject            = request.POST['subject']
            testdate           = request.POST['testdate']
            description        = request.POST['description']

            if not Class.objects.filter(class_no=forclass, school=request.user.school).exists():
                messages.warning(request, "The class does not exists.")
                return redirect('/dashboard/uploadtest')

            if subject != 'Urdu' and subject != 'English' and subject != 'Maths' and subject != 'Physics' and subject != 'Chemistry' and subject != 'Bio' and subject != 'Computer' and subject != 'Pak-Studies' and subject != 'Science' and subject != 'Islamiyat' and subject != 'Arabic':
                messages.warning(request, "Invalid subject.")
                return redirect('/dashboard/uploadtest')


            myclass            = Class.objects.get(class_no=forclass, school=request.user.school)
            mytest             = Upcoming_Test(subject=subject, description=description, date=testdate, for_class=myclass)
            mytest.save()

            messages.success(request, "Test has been uploaded successfully")
            return redirect('/dashboard/uploadtest')
    else:
        return redirect('notfound')

def upcomingtest(request, Id):
    if request.user.is_authenticated:
        myclass            = Class.objects.get(id=Id)
        tests              = Upcoming_Test.objects.filter(for_class=myclass).order_by('-id')
        return render(request, 'dashboard/upcomingtest.html', {'tests':tests})
    else:
        return redirect('notfound')

#for deleting upcoming test
def deletetest(request, Id):
    test = Upcoming_Test.objects.get(id=Id)
    myclass = test.for_class
    classid = myclass.id
    test.delete()
    messages.success(request, "test has been deleted successfully")
    return redirect('upcomingtest', classid)    
