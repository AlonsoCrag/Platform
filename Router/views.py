from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
# Class based
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
# Models
from .models import Routes
# Dotenv
from dotenv import load_dotenv
import os

# Create your views here.
def Initial(request):
    return JsonResponse({"Working": True})


# Special route to add routes to the model faster and easier
class AddRoute(TemplateView):
    def get(self, request, *args, **kwargs):
        # print(request.GET)
        # print(len(request.GET))
        if 'name' in request.GET and len(request.GET) == 3:
            # print("You can save into your model")
            content = request.GET
            Rt = Routes(Name=content["name"], Path=content["path"] + "/", Extra=content["extra"])
            Rt.save()
            # print("--Done--")
        return JsonResponse({"Info":"Route was added"}) 


class Pages(ListView):
    model = Routes
    context_object_name = "records"
    template_name = 'pages.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["Acces"] = "General"
        data["Host"] = Host_Env()
        data["Url"] = "pages/"
        # print("Data obtanined", data)
        return data




def Login(request):
    return JsonResponse({"login": False})



def Host_Env():
    isFile = load_dotenv(dotenv_path="../.env")
    # print(".env was Found?", isFile)
    return os.getenv("HOST")



