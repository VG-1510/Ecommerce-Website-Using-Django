from django.db import models

# Create your models here.
class users(models.Model):
    firstname = models.CharField(max_length = 255)
    lastname = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    cart = models.JSONField(default="[]")
    
    # [12,5,78]
    def __str__(self):
        return f"{self.firstname} {self.lastname}"