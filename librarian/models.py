from django.db import models
from school.models import School,BookExtra
from reader.models import Reader
# Create your models here.
class Librarian(models.Model):
    username=models.CharField(max_length=12,primary_key=True)
    password=models.CharField(max_length=18)
    name=models.CharField(max_length=25)
    age=models.IntegerField()
    school=models.ForeignKey(School,on_delete=models.CASCADE)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Issue(models.Model):
    book_id=models.ForeignKey(BookExtra,on_delete=models.CASCADE)
    student_id=models.ForeignKey(Reader,on_delete=models.CASCADE)
    issueDate=models.DateField()
    returnDate=models.DateField()
    reference=models.IntegerField(default=0)
    status=models.CharField(max_length=15,default='missing')

    def __str__(self):
        return str(self.reference)

class RequestBook(models.Model):
    student_id=models.ForeignKey(Reader,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    time=models.DateField()
    reason=models.CharField(max_length=30,default='out of stock')
    def __str__(self):
        return self.name