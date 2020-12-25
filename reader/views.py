from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from reader.models import Reader,Treader,Referral,Requestt
from school.models import Book,BookExtra,School
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view
import json
from datetime import datetime,date,timedelta
from librarian.models import Issue,RequestBook
from reader.serializers import Bookserializer
import random
from django.core.mail import send_mail
from django.utils.html import strip_tags
from reader.extrafunctions import encrypt
from event.models import Festorder
# Create your views here.
action=[{"name":"view books","link":""},{"name":"profile","link":"profile"},{"name":"request","link":"request"},{"name":"orders and requests","link":"view_order"}]
# submenu=[{"name":"class 6","subcategory":['Maths','Science']},{"name":"class 6","subcategory":['Maths','Science']}]
submenu=['Maths','Science','History']
def login(request):
    if('reader' in request.session):
        return redirect('event_home')
    if(request.method == 'GET'):
        params={"action":action,'type':'reader','Error':''}
        return render(request, 'login.html', params)
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        try:
            details = Reader.objects.get(username=username)
            if(details.password == password):
                request.session['reader'] = username
                return redirect('event_home')
            else:
                params={"action":action,'type':'reader','Error':'Either username or password is incorrect'}
                return render(request,'login.html',params)
        except:
            params={"action":action,'type':'reader','Error':'Either username or password is incorrect'}
            return render(request,'login.html',params)

def signup(request):
    if('reader' in request.session):
        return redirect('reader_home')
    if(request.method=='GET'):
        params={'action':action,'type':'reader','Error':False}
        return render(request,'signup.html',params)
    if(request.method=='POST'):
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        username=request.POST['username']
        password=request.POST['password']
        age=request.POST['age']
        scl=School.objects.get(username='cts')
        otp=random.randint(10000,999999)
        treader=Treader(username=username,otp=str(otp),status='pending')
        treader.save()
        rdr=Reader.objects.filter(username=username)
        Error=[]
        t=loader.get_template('emailverify.html')
        if(len(rdr)!=0):
            Error.append("Username not available.")
        rdr=Reader.objects.filter(email=email)
        if(len(rdr)!=0):
            Error.append("Email is already registered.")
        rdr=Reader.objects.filter(phone=phone)
        if(len(rdr)!=0):
            Error.append("Phone is already registered.")
        if(Error):
            params={'action':action,'type':'reader','Error':Error}
            return render(request,'emailverify.html',params)
        params={'action':action,'type':'reader','Error':Error,'mail':email}
        resp=HttpResponse(t.render(params,request))
        for key,item in request.POST.items():
            resp.set_cookie(key,item,max_age=15*60)
        html_message=render_to_string('mail/otp.html',{'name':name,'otp':otp})
        plain_message=strip_tags(html_message)
        send_mail('ConnecTheShelf verification',plain_message,'deepprak2001@gmail.com',[email],html_message=html_message,fail_silently=False)
        return resp

        
def verify(request):
    if(request.method=='POST'):
        otp=request.POST['otp']
        username=request.COOKIES['username']
        name=request.COOKIES['name']
        age=request.COOKIES['age']
        phone=request.COOKIES['phone']
        password=request.COOKIES['password']
        email=request.COOKIES['email']

        treader=Treader.objects.filter(username=username).last()
        if(treader.otp==otp):
            treader.status='successfull'
            treader.save()
            treader.delete()
            scl=School.objects.get(username='cts')
            rdr=Reader(name=name,username=username,age=age,password=password,phone=phone,email=email,school=scl)
            rdr.save()
            ref=Referral(username=rdr,code=encrypt(username),usage=0)
            ref.save()
            return redirect('reader_login')
        else:
            treader.status='unsucessfull'
            treader.delete()
            params={'action':action,'type':'reader','Error':["otp didn't matched"]}
            return render('emailverify.html',params)
    return HttpResponse(404)

def home(request):
    return redirect('event_home')
    # params={"action":action,'type':'reader'}
    # return render(request, 'student/home.html',params)

@api_view(['GET','POST'])
def fetchbook(request):
    if(request.method=='POST'):
        typef=request.data['type']
        category=request.data['category']
        if(typef!='ALL' and category!='ALL'):
            obj=Book.objects.filter(standard=typef,topic=category)
        elif(typef=='ALL' and category!='ALL'):
            obj=Book.objects.filter(topic=category)
        elif(typef!='ALL' and category=='ALL'):
            obj=Book.objects.filter(standard=typef)
        else:
            obj=Book.objects.all()
        lst=list(obj)
        serializer = Bookserializer(lst, many=True)
        # print(serializer.data)

        return JsonResponse(serializer.data,safe=False)
        


@api_view(['GET','POST'])
def order(request):
    if(request.method=='POST'):
        books=request.data['books']
        reference=request.data['reference']
        st=Reader.objects.get(username=request.session['reader'])
        for book in books:
            bookName=Book.objects.get(name=book)
            bk=BookExtra.objects.filter(name=bookName,status='available').first()            
            date_1 = datetime.strptime(date.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
            end_date = date_1 + timedelta(days=10)
            bk.status='pending'
            bk.save()
            iss=Issue(book_id=bk,student_id=st,issueDate=date.today().strftime('%Y-%m-%d'),returnDate=end_date,reference=reference,status='pending')
            iss.save()

        params={"response":True,"reference":reference}
        return JsonResponse(params,safe=False)

@api_view(['GET','POST'])
def getstock(request):
    if(request.method=='POST'):
        name=request.data['name']
        scl=Reader.objects.get(username=request.session['reader'])
        scl=scl.school
        bk=Book.objects.get(name=name)
        bookstock=BookExtra.objects.filter(name=bk,owner=scl,status='available')
        stock={'stock':len(bookstock)}
        return JsonResponse(stock)

def viewOrder(request):
    if('reader' in request.session):
        if(request.method=='GET'):
            fst=Festorder.objects.filter(userid=request.session['reader'])[::-1]
            addr=Reader.objects.filter(username=request.session['reader']).first()
            params={'action':action,'type':'reader','fst':fst,'address':addr.address}
            return render(request,'student/orderrequest.html',params)
    if(request.method=='POST'):
        username=request.session['reader']
        username=Reader.objects.get(username=username)
        name=request.POST['name']
        author=request.POST['author']
        reason=request.POST['reason']
        st=Reader.objects.get(username=request.session['reader'])
        issues=list(Issue.objects.filter(student_id=st))
        issues=issues[::-1]
        rq=RequestBook(username=username,name=name,author=author,reason=reason,time=date.today())
        rq.save()
        params={'action':action,'type':'reader','issues':issues,'message':'submitted successfully'}
        return render(request,'student/orderrequest.html',params)
    return redirect('reader_login')

def profile(request):
    if('reader' in request.session):
        if(request.method=='GET'):
            rdr=Reader.objects.get(username=request.session['reader'])
            ref=Referral.objects.get(username=rdr)
            params={'action':action,'type':'reader','reader':rdr,'ref':ref}
            return render(request,'student/profile.html',params)

        if(request.method=='POST'):
            name=request.POST['name']
            age=request.POST['age']
            password=request.POST['password']
            phone=request.POST['phone']
            address=request.POST['address']
            rdr=Reader.objects.get(username=request.session['reader'])
            email=rdr.email
            rdr.name=name
            rdr.age=age
            rdr.password=password
            rdr.address=address
            rdr.save()
            html_message=render_to_string('mail/changedetails.html',{'name':name})
            plain_message=strip_tags(html_message)
            send_mail('ConnecTheShelf Change profile',plain_message,'deepprak2001@gmail.com',[email],html_message=html_message,fail_silently=False)
            return redirect('profile')
        return redirect('profile')

def requestt(request):
    if 'reader' in request.session:
        if(request.method=='GET'):
            params={'action':action,'type':'reader'}
            rdr=Reader.objects.get(username=request.session['reader'])
            fst=Requestt.objects.filter(username=rdr)[::-1]
            params['fst']=fst
            return render(request,'request.html',params)

        if(request.method=='POST'):
            name=request.POST['bookname']
            author=request.POST['authorname']
            rdr=Reader.objects.get(username=request.session['reader'])
            req=Requestt(name=name,author=author,username=rdr,status='pending')
            req.save()
            return redirect('request')
    return redirect('reader_login')