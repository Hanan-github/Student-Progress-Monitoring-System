from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_parent', 'is_school']
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
