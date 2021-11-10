from django.db import models
from Register.models import RegisterModel, validate_field

# Create your models here.
class Storie(models.Model):
    Title = models.CharField(max_length=100)
    Body = models.CharField(max_length=700)
    Image = models.ImageField(upload_to="storie_img")
    Owner = models.CharField(max_length=100)

    def __str__(self):
        return self.Title