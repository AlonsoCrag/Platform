from django.db import models

# Create your models here.
class Routes(models.Model):
    Name = models.CharField(max_length=100)
    Path = models.CharField(max_length=100)
    Extra = models.CharField(max_length=100)

    def __str__(self):
        return self.Name
