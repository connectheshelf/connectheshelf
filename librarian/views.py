from django.shortcuts import render,redirect,HttpResponse
from librarian.models import Librarian,Issue,RequestBook
from school.models import Book,BookExtra,School
from reader.models import Reader
from datetime import date,datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
# Create your views here.

action = [
    {"name": "issue a book", "link": "issue"},
    {"name": "return a book", "link": "return"},
    {"name": "track book record", "link": "trackbook"},
    {"name": "track student record", "link": "trackstudent"},
    {"name": "get summary", "link": "summary"},
    {"name": "verify submitted", "link": "verify"},
]

def login(request):
    if('librarian' in request.session):
        return redirect('librarian_home')
    if(request.method == 'GET'):
        return render(request, 'login.html',{'type':'librarian'})
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']
        try:
            details=Librarian.objects.get(username=username)
            if(details.password==password):
                request.session['librarian']=username
                return redirect('librarian_home')
        except:
            return redirect('home')



def home(request):
    params={"action":action}
    issues=Issue.objects.all()
    lst=list(issues)
    lst=lst[::-1]
    params['issues']=lst
    params['type']='librarian'
    return render(request,'library/librarian.html',params)

def trackbook(request):
    params = {"action": action}
    params['type']='librarian'
    params['typeof']='book'
    if(request.method=='GET'):
        return render(request,'library/trackrecord.html',params)
    if(request.method=='POST'):
        params = {"action": action}
        params['type'] = 'librarian'
        params['typeof'] = 'book'
        username=request.POST['username']
        issue=Issue.objects.filter(book_id_id=username)
        lst=list(issue)
        print(lst)
        lst=lst[::-1]
        params['issues']=lst
        return render(request,'library/trackrecord.html',params)


def trackstudent(request):
    params = {"action": action}
    params['type'] = 'librarian'
    params['typeof'] = 'student'
    if(request.method == 'GET'):
        return render(request, 'library/trackrecord.html', params)
    if(request.method == 'POST'):
        params = {"action": action}
        params['type'] = 'librarian'
        params['typeof'] = 'student'
        username = request.POST['username']
        issue = Issue.objects.filter(student_id_id=username)
        lst = list(issue)
        lst=lst[::-1]
        params['issues'] = lst
        return render(request, 'library/trackrecord.html', params)

    # params={"action":action}
    # params['type']='librarian'
    # return render(request,'library/trackrecord.html',params)

def fake(request):
    for i in range(2,6):
        scl = School.objects.get(name='abc school')
        book = Book(name='book'+str(i),author='author'+str(i),cover='book1.jpg',description='Donec mattis tincidunt ipsum vel efficitur. Aliquam aliquam interdum rhoncus. Nam nec condimentum dolor, et pharetra nisi. In feugiat felis nec erat eleifend condimentum. Aliquam egestas convallis eros sed gravida. Curabitur consequat sit amet neque ac ornare',topic='Maths',standard=6)
        book.save()
        for j in range(4):
            book_extra=BookExtra(name=book,book_id=i*j,confirmation_id=i*j*2,owner=scl)
            book_extra.save()
    return HttpResponse('hello')


@api_view(['GET','POST'])
def returnBook(request):
    if(request.method=='GET'):
        params = {"action": action}
        return render(request,'library/return.html',params)
    if(request.method=='POST'):
        books=request.data['returnbooks']
        books=books.split("\r\n")
        params = {"action": action}
        bk=[]
        res=[]
        for book in books:
            bk1=book.split()
            bk.append(bk1)
        for item in bk:
            tempres={'id':item[0]}
            try:
                bks=BookExtra.objects.filter(book_id=item[0],confirmation_id=item[1]).first()
                iss=Issue.objects.filter(book_id=bks,status='delivered').first()
                if(iss.returnDate<date.today()):
                    iss.status='late'
                else:
                    iss.status='submitted'
                bks.status='returned'
                bks.save()
                iss.save()
                tempres['status']=True
            except Exception as e:
                tempres['status']=False
            res.append(tempres) 
        return JsonResponse(res,safe=False)

def issueBook(request):
    params={"action":action}
    params['type']='librarian'
    if(request.method=='GET'):
        return render(request,'library/issue.html',params)
    if(request.method=='POST'):
        reference=request.POST['reference']
        username=request.POST['username']
        params['action']=action
        issue=Issue.objects.filter(reference=reference,student_id_id=username,status='pending')
        lst=list(issue)
        for issue in lst:
            issue.status='delivered'
            issue.save()
        params['issues']=lst
    return render(request,'library/issue.html',params)

def summary(request):
    params={"action":action}
    scl=Librarian.objects.get(username=request.session['librarian'])
    scl=scl.school
    issues=[]
    nissues=Issue.objects.filter().all()
    nissues=len(nissues)
    requ=RequestBook.objects.filter().all()
    requ=list(requ)
    requ=requ[::-1]
    params['issues']=requ
    params['nissue']=nissues
    params['nrequests']=len(requ)
    params['ratings']=((len(issues)+0.0)/(len(requ)+len(issues)))*5
    print(params['ratings'])
    return render(request,'library/record.html',params)

def printpage(request):
    if(request.method=='POST'):
        data=request.POST['data']
        text={'text':data,'time':datetime.now()}
        return render(request,'print.html',text)
