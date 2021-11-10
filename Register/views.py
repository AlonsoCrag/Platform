from django.http.response import HttpResponse
from django.shortcuts import render
from .models import RegisterModel
from .forms import RegisterForm
from .HashPass import Hash
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
# Models
from Router.models import Routes
# Create your views here.
def Register(request):
    context = {
        "form": RegisterForm()
    }

    context["Pages"] = Routes.objects.all()
    context["Url"] = "register/"

    if 'success' in request.GET:
        context.pop("form")
        context["success"] = "Congrats, you have registered succesfully"
    
    if request.method == "POST":
        Form = RegisterForm(request.POST, request.FILES)

        if Form.is_valid():
            print("For was validated")
            print(Form.cleaned_data)
            HPass = Hash(Form.cleaned_data["Password"])
            keyPass, salt = HPass.hash_data()
            print("Key", keyPass)
            print("Salt", salt)

            # Save into the model
            try:
                res = RegisterModel.objects.get(Username=Form.cleaned_data["Username"])
                print("Res", res)
            except:
                User = RegisterModel(Username=Form.cleaned_data["Username"], Lastname=Form.cleaned_data["Lastname"], 
                Password=str(keyPass), Salt=str(salt), Picture=Form.cleaned_data["Picture"])
                User.save()
            else:
                context["error_username"] = "Username is already taked"
                context["form"] = RegisterForm(request.POST)
                return render(request, 'register.html', context)

            return HttpResponseRedirect('/register/?success=true')

        context["error_password"] = "Password should be greater than 5 characters"
        context["form"] = RegisterForm(request.POST, request.FILES)
        # return HttpResponse("DEV_ERROR: You are not filling the form with request.FILES in case you are using files")
            
    return render(request, 'register.html', context)