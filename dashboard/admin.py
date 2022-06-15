from django.contrib import admin
from dashboard.models import School, Student, Parent, Result_Card, Attendence_Report, Upcoming_Test, Class, Event



# Register your models here.

admin.site.register(School)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Result_Card)
admin.site.register(Attendence_Report)
admin.site.register(Upcoming_Test)
admin.site.register(Class)
admin.site.register(Event)

