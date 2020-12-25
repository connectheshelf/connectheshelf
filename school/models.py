from django.db import models

# Create your models here.
class School(models.Model):
    username=models.CharField(max_length=15)
    password=models.CharField(max_length=18)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    pincode=models.CharField(max_length=6)

    def __str__(self):
        return self.name

class Book(models.Model):
    name=models.CharField(max_length=20,primary_key=True)
    author=models.CharField(max_length=20)
    cover=models.ImageField(upload_to='static/books')
    description=models.CharField(max_length=400)
    topic=models.CharField(max_length=40,default='ALL')
    standard=models.IntegerField(default=6)
    
    def __str__(self):
        return self.name

class BookExtra(models.Model):
    book_id=models.CharField(max_length=8,primary_key=True)
    confirmation_id=models.CharField(max_length=8)
    name=models.ForeignKey(Book,on_delete=models.CASCADE)
    owner=models.ForeignKey(School,on_delete=models.CASCADE)
    status=models.CharField(max_length=10,default='available')
    def __str__(self):
        return self.book_id
