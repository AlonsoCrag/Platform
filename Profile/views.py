from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from numpy.compat.py3k import contextlib_nullcontext
# Model User
from Register.models import RegisterModel
# Rest_Framework
from rest_framework import serializers
from site_backend.settings import BASE_DIR
# Form Story
from .forms import CreateStory, EditProfile
# Model Story
from .models import Storie
# Pillow
from PIL import Image
from django.conf import settings
import numpy
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import urls
# Password Hash Structur
from Register.HashPass import HashWithSalt, Hash
# Download Files
import os
from django.conf import settings
import mimetypes

# Create your views here.
def Profile(request):
    try:
        print(request.session["user"])
    except:
        return HttpResponse("Empty")
    else:
        print("Profile Request Session", request.session["user"])
        QuerySet = RegisterModel.objects.filter(Username=request.session["user"])
        print("User Data", QuerySet)
        DataSerialized = SerializeData(QuerySet[0])
        context = DataSerialized.data
        context["CreateStory"] = CreateStory()
        
        User = RegisterModel.objects.get(Username=request.session["user"])
        if (User.AllowGif):
            context["GifPicture"] = context["GifPath"]

        print("URLS", urls)

        if len(Storie.objects.all()) != 0:
            context["Cards"] = Storie.objects.filter(Owner = context["Username"])
            print("Length of list cards", len(context["Cards"]))

        if request.method == 'POST':
            Form = CreateStory(request.POST, request.FILES)
            if Form.is_valid():
                data = Form.cleaned_data

                _file = ImageTransform(Form.cleaned_data["Image"])
                Form.cleaned_data["Image"].file = _file
                Storie(Title = data["Title"], Body = data["Body"], Image = Form.cleaned_data["Image"], Owner = context["Username"]).save()

                print("New story has been created", Form.cleaned_data)
                context["NewStory"] = "Done"
                context["Cards"] = Storie.objects.filter(Owner = context["Username"])
                return render(request, 'user.html', context)
            

        return render(request, 'user.html', context)


class SerializeData(serializers.ModelSerializer):
    class Meta:
        model = RegisterModel
        fields = ["Username", "Lastname", "Picture", "GifPath"]

    
def ImageTransform(image):
    image = Image.open(image)
    source = image.convert("RGB")
    source = source.resize((140, 100))
    output = BytesIO()
    source.save(output, format="JPEG")
    output.seek(0)
    # print(output.read())
    # img = numpy.array(image)
    # print(img.shape)
    content = ContentFile(output.read())
    _file = File(content)
    return _file


def  Edit(request, username):
    context = {
            "Form": EditProfile()
    }
    try:
        user_sid = request.session["user"]
    except:
        return HttpResponse("You must log or create an account before you try this feature ;)")
    else:
        if request.method == 'POST':
            User = RegisterModel.objects.get(Username=request.session["user"])
            Form = EditProfile(request.POST, request.FILES)
            if Form.is_valid():
                DataManager = ChangePassword(request, Form.cleaned_data, User)
                DataManager.get_params()
                DataManager.change_in_model()
                if not DataManager.is_correct_password():
                    context["error_password"] = "Current password don't match"
                    return render(request, 'edit.html', context)
                return HttpResponseRedirect(f'/edit/user/{request.session["user"]}')
        return render(request, 'edit.html', context)


class ChangePassword:
    def __init__(self, request, data, userRecord):
        self.request = request
        self.data = data
        self.userRecord = userRecord
        self.password = None
        self.salt = None
        self.pass_query = None

    def get_params(self):
        self.password = eval(self.userRecord.Password)
        self.salt = eval(self.userRecord.Salt)
        # print(f"Salt -> {self.salt} Password -> {self.password}")

    def change_in_model(self):
        password = HashWithSalt(self.data["OldPassword"], self.salt).hash_data()
        if password == self.password:
            passw, salt = Hash(self.data["NewPassword"]).hash_data()
            self.userRecord.Password = str(passw)
            self.userRecord.Salt = str(salt)
            self.pass_query = True
        else:
            self.pass_query = False
        if self.data["Username"] != None and self.data["Username"] != '':
            print("Username has changed", type(self.data["Username"]))
            self.userRecord.Username = self.data["Username"]
            try:
                self.userRecord.save()
            except:
                print("Error while trying to update the user")
            else:
                # update the request.session["user"] once the username has changed
                self.update_session_token()
        if self.data["GifPath"] != None and self.data["GifPath"] != '':
            self.userRecord.AllowGif = True
            self.userRecord.GifPath = self.data["GifPath"]
        if self.data["Picture"] != None and self.data["Picture"] != '':
            self.userRecord.Picture = self.data["Picture"]    

        self.userRecord.save()

    def is_correct_password(self):
        if not self.pass_query:
            return False
        return True

    def update_session_token(self):
        self.request.session["user"] = self.data["Username"]
        print("New token sid", self.request.session["user"])
    




def Download(request):
    BASE_DIR = settings.BASE_DIR
    filename = 'python.exe'
    path = str(BASE_DIR) + f'/media/storie_img/{filename}'
    print("--------------------------")
    _file = open(path, 'rb')
    print("-------------------------- 22222222222222")
    mime_type, _ = mimetypes.guess_type(path)
    print("-------------------------- 33333333333", mime_type)
    response =  HttpResponse(_file, content_type=mime_type)
    print("-------------------------- 4444444444")
    # response["Content-Disposition"] = 'attachment: filename=%s' % 'spiderman.jpg'
    response['Content-Disposition'] = f"attachment; filename={filename}"
    return response