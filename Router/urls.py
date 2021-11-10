from django.urls import path
from . import views
from Register.views import Register
from Login.views import Login
from Profile.views import Profile, Edit, Download

urlpatterns = [
    path('test/', views.Initial, name="Route for testing purposes"),
    path('addRoute/', views.AddRoute.as_view()),
    path("pages/", views.Pages.as_view()),
    path("register/", Register),
    path("login/", Login),
    path('', Profile),
    path('edit/user/<str:username>', Edit),
    path('downloadFiles/', Download)
]

