from django.contrib import admin
from .models import RegisterModel
# Register your models here.

def info(model, request, querySet):
    print(model, request)
    for query in querySet:
        print(query.Username)

class Data(admin.ModelAdmin):
    actions = (info,)
    list_display = ["id", "Username", "Lastname"]

admin.site.register(RegisterModel, Data)