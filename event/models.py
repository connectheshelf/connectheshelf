from django.db import models
from reader.models import Reader
# Create your models here.

class Festbook(models.Model):
    bookid=models.CharField(max_length=10)
    name=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    category=models.CharField(max_length=20)
    price=models.FloatField(default=0,null=True)
    image=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Festorder(models.Model):
    userid=models.ForeignKey(Reader,on_delete=models.CASCADE)
    orderId=models.CharField(max_length=50)
    bookid=models.CharField(max_length=10)
    coupon=models.CharField(max_length=12,default='000',null=True)
    tme=models.DateTimeField()
    status=models.CharField(max_length=10,default='pending')
    oldbook=models.IntegerField(default=0)
    express=models.IntegerField(default=0)
    address=models.TextField()
    def __str__(self):
        return self.orderId
