from django.contrib import admin
from .models import Routes
from CustomAdmin.admin import site

# admin.site = site

def get_data(model, querySet, request):
    print(querySet)

# Register your models here.
class Visual(admin.ModelAdmin):
    list_display = ["Name", "Path", "Extra"]
    actions = (get_data,)

admin.site.register(Routes, Visual)