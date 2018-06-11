from django.contrib import admin
from .models import UserProfile, ToDo

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ToDo)