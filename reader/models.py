from django.db import models
from school.models import School
# Create your models here.
class Reader(models.Model):
    username=models.CharField(max_length=12,primary_key=True)
    password=models.CharField(max_length=18)
    age=models.IntegerField()
    name=models.CharField(max_length=15)
    email=models.CharField(max_length=25)
    phone=models.CharField(max_length=15)
    std=models.IntegerField(default=0)
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    address=models.TextField(default="Not provided")
    def __str__(self):
        return self.name

class Treader(models.Model):
    username=models.CharField(max_length=12)
    otp=models.CharField(max_length=8,default='000000')
    status=models.CharField(default='pending',max_length=10)

    def __str__(self):
        return self.username

class Referral(models.Model):
    username=models.ForeignKey(Reader,on_delete=models.CASCADE)
    code=models.CharField(max_length=12,default=username.name)
    usage=models.IntegerField(default=0)

    def __str__(self):
        return self.code

class Requestt(models.Model):
    username=models.ForeignKey(Reader,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    author=models.CharField(max_length=100)
    status=models.CharField(max_length=10)
