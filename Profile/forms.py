from django import forms
from django.forms import TextInput, PasswordInput, FileField
from django.forms.widgets import Textarea
from .models import Storie
from django.forms import Textarea, CharField

class CreateStory(forms.ModelForm):
    class Meta:
        model = Storie
        fields = ["Title", "Body", "Image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Fields in Story Form", self.fields)
        self.change_fields()
        
    def change_fields(self):
        self.fields["Body"] = CharField(max_length=700, widget=Textarea)
        self.fields["Title"].widget.attrs.update({"placeholder": "Title", "class": "form-control"})
        self.fields["Body"].widget.attrs.update({"placeholder": "History", "class": "form-control text-left", "style": "height: 100px;"})
        self.fields["Image"].widget.attrs.update({"class": "btn btn-secondary form-control"})


class EditProfile(forms.Form):
    Username = forms.CharField(max_length=100, required=False, widget=TextInput(attrs={"class": "form-control"}))
    OldPassword = forms.CharField(max_length=100, required=False, widget=PasswordInput(attrs={"class": "form-control"}))
    NewPassword = forms.CharField(max_length=100, required=False, widget=PasswordInput(attrs={"class": "form-control"}))
    GifPath = forms.CharField(max_length=400, required=False, widget=TextInput(attrs={"class": "form-control"}))
    Picture = forms.ImageField(required=False)
