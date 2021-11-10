from django.db import models
from django.forms import PasswordInput
from django.core.exceptions import ValidationError

def validate_field(value):
    print("Calling method validate_field()", value)
    if ("Dumb" in value):
        print("Badword detected")
        raise ValidationError("You can not use badwords as Username, srry :C")

def validate_pass(value):
    print("Length of password is", len(value))
    if len(value) <= 5:
        raise ValidationError("Password is too small")

# Create your models here.
class RegisterModel(models.Model):
    Username = models.CharField(max_length=50, validators=[validate_field])
    Lastname = models.CharField(max_length=50)
    Picture = models.ImageField(upload_to="pictures")
    Password = models.CharField(max_length=400, default='', validators=[validate_pass])
    Salt = models.CharField(max_length=500, default='')
    AllowGif = models.BooleanField(default=False)
    GifPath = models.TextField(default='')

    def esample(self):
        pass

    def __str__(self):
        return self.Username

# Use validators for your fields to process the data before saving it into the database
# The validators functions gets called when we Create an Instance of the model and provide the values for each field
# If we raise a ValidationError(value) -> The process of saving the data to the database will be truncated


# Also functions of validators, if you are using them to create a form with "forms.ModelForm" class
# Those functions also works in the forms to validate the data thats amazing

