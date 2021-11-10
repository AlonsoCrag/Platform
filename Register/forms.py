from .models import RegisterModel
from django import forms
from django.forms import PasswordInput # Special class to change attributes in a field

customField = forms.CharField(max_length=100, widget=PasswordInput)

class RegisterForm(forms.ModelForm):
    class Meta:
        model = RegisterModel
        fields = ("Username", "Lastname", "Password", "Picture")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Init method in form class")
        print(self.fields)
        self.fields["Password"] = customField
        self.fields["Username"].widget.attrs.update({'placeholder': "Username", "class": "form-control"}) # Updating attributes of fields
        self.fields["Password"].widget.attrs.update({'placeholder': "Password", "class": "form-control"})
        self.fields["Lastname"].widget.attrs.update({"placeholder": "Lastname", "class": "form-control"})
        self.fields["Picture"].widget.attrs.update({"class": "form-control"})
        # self.fields.pop("Password")
        # Remember that self.fields is an attribute that comes from the parent class in his __init__() method
        # Wich is a dictionary and u can assign new keys (new fields) and as values (fields that django.forms allows to use)
        # The above code works, it adds a new fields of tyep CharField, since Charfield comes straight from the django.forms Module
