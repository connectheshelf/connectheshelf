from django.db import models

# Create your models here.
class Donation(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    contact=models.CharField(max_length=10)
    book=models.TextField()
    address=models.TextField()

class Contact(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    contact=models.CharField(max_length=10)
    title=models.CharField(max_length=50)
    message=models.TextField()
