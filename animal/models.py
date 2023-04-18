from django.db import models


# Create your models here.
class Animal(models.Model):
    name = models.CharField(max_length=50)
    sound = models.CharField(max_length=50)
    size = models.CharField(max_length=3, default="sml")
    age = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def speak(self):
        return self.name + " speaks " + self.sound

    def howBig(self):
        return self.size
