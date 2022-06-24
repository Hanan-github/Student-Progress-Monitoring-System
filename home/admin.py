from django.contrib import admin
from home.models import Contact

# Register your models here.
admin.site.register(Contact)
admin.site.site_header = 'SPMS Admin Panel'