from django.db import models
from django.utils.timezone import now  # Import to get the current time

class MissingPerson(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    height = models.FloatField()
    description = models.TextField()
    language = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='missing_persons/')
    
    # Fields for case registrant information with default values
    case_registered_by = models.CharField(max_length=255, default="Admin")  # Default name of registrant
    phone_number = models.CharField(max_length=15, default="000-000-0000")  # Default phone number
    email = models.EmailField(max_length=30, default="example@gmail.com")  # Default email
    address = models.CharField(max_length=255, default="Unknown Address")  # Default address
    
    # DateTime field with default as the current time
    case_registered_at = models.DateTimeField(default=now)  # Default current time

    def __str__(self):
        return self.name
