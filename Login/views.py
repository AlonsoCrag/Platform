from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Form Login
from .forms import LoginForm
# Model to verify users in the database table / model
from Register.models import RegisterModel
# Model to get the Pages
from Router.models import Routes
# Serializers / djangorestframework
from rest_framework import serializers
# Hash to obtain the key
import hashlib

# Create your views here.
def Login(request):
    try:
        del request.session["user"]
        print("request.session was erased")
    except:
        pass
    context = {
        "form": LoginForm()
    }
    context["Pages"] = Routes.objects.all()
    context["Url"] = "login/"

    check_dark_mode(request.COOKIES, context)

    if request.method == "POST":
        Form = LoginForm(request.POST)
        if Form.is_valid():
            Data = Form.cleaned_data
            Query = RegisterModel.objects.filter(Username=Data["Username"])
            data = Serialize_Records(Query)

            if data == False:
                context["error_login"] = "Wrong password or username"
                return render(request, "login.html", context)



            Key_in_model = eval(data["Password"])
            Salt_in_model = eval(data["Salt"])

            print("Salt", Salt_in_model)

            key_in_log = Obtain_Password_Key(Data["Password"], Salt_in_model)

            print("KeyModel", Key_in_model)
            print("KeyToLog", key_in_log)
            
            if Success_Redirect(key_in_log, Key_in_model):
                request.session['user'] = data["Username"]
                # request.session["spiderman"] = "Some sid here"
                # del request.session["extra"]
                return HttpResponseRedirect('/')
            
            context["error_login"] = "Wrong password or username"

            

    return render(request, "login.html", context)


# Model to serialize the data of QuerySets to get python Native objects that can be easily stored in json format
class SerializerRecords(serializers.ModelSerializer):
    class Meta:
        model = RegisterModel
        fields = ("Username", "Lastname", "Password", "Salt")



def Serialize_Records(query_set):
    if len(query_set) != 0:
        serializer = SerializerRecords(query_set[0])
        return serializer.data
    return False


def Obtain_Password_Key(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations=10000)


def Success_Redirect(keyLog, keyModel):
    if keyModel == keyLog:
        print("Success and redirect")
        return True


def check_dark_mode(cookies, context):
    if "mode" in cookies:
        print("Dark mode was enabled")
        context["darkMode"] = "bg-dark text-white"