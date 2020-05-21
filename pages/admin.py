from django.contrib import admin

# Register your models here.
from .models import Contact, Project

admin.site.register(Contact)
admin.site.register(Project)
