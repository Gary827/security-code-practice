from urllib.response import addinfo
from django.contrib import admin
from commonauth.models import *

class CommonUserAdmin(admin.ModelAdmin):
    list_display = ['userid','username','hobby']
    
admin.site.register(CommonUser, CommonUserAdmin)