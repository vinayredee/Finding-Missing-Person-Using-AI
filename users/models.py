from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200, unique=True, default="default_username")
    email = models.EmailField(unique=True, default="example@gmail.com")
    pass1 = models.CharField(max_length=16, default="password1234")  # Default password for testing or placeholder
    pass2 = models.CharField(max_length=16, default="password1234")  # Default password for testing or placeholder

    def __str__(self):
        return self.username
