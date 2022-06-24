from django.contrib import admin
from dashboard.models import School, Student, Parent, Result_Card, Attendence_Report, Upcoming_Test, Class, Event

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'account']

class ParentAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 'cnic', 'account']

class ClassAdmin(admin.ModelAdmin):
    list_display = ['class_no', 'class_title', 'school']

class UpcomingtestAdmin(admin.ModelAdmin):
    list_display = ['subject', 'date', 'for_class']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'roll_number', 'father_cnic', 'student_class', 'school', 'parent']

class AttendenceReportAdmin(admin.ModelAdmin):
    list_display = ['student', 'Date', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Monday']

class ResultCardAdmin(admin.ModelAdmin):
    list_display = ['student', 'date']

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'school']

# Register your models here.

admin.site.register(School, SchoolAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Result_Card, ResultCardAdmin)
admin.site.register(Attendence_Report, AttendenceReportAdmin)
admin.site.register(Upcoming_Test, UpcomingtestAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Event, EventAdmin)

