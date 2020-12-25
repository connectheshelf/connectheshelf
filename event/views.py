from django.shortcuts import render, HttpResponse
from event.models import Festbook, Festorder
from django.http import JsonResponse
from reader.models import Referral,Reader
from rest_framework.decorators import api_view
from event.serializers import Festserializer
from reader.extrafunctions import encrypt
from datetime import datetime
action=[{"name":"view books","link":""},{"name":"profile","link":"profile"},{"name":"request","link":"request"},{"name":"orders and requests","link":"view_order"}]
# Create your views here.
def home(request):
    if('reader' in request.session):
        params={'action':action,'type':'reader'}
    else:
        params={'type':'reader'}
    fst=Festbook.objects.filter(category='novel')[::10]
    params['novel']=list(fst)
    fst=Festbook.objects.filter(category='literature')[::2]
    params['literature']=list(fst)
    fst=Festbook.objects.filter(category='thriller')[::5]
    params['thriller']=list(fst)
    fst=Festbook.objects.filter(category='exam')[::5]
    params['exam']=list(fst)
    fst=Festbook.objects.filter(category='comics')[::5]
    params['comics']=list(fst)
    fst=Festbook.objects.filter(category='religion')[::5]
    params['religion']=list(fst)
    return render(request,'event.html',params)

def view(request,category):
    if('reader' in request.session):
        params = {'action': action, 'type': 'reader'}
    else:
        params={'type':'reader'}
    fst=Festbook.objects.filter(category=category)
    params['fst']=list(fst)
    params['category']=category
    return render(request,'viewall.html',params)

@api_view(['GET','POST'])
def getorder(request):
    if('reader' in request.session):
        params = {'action': action, 'type': 'reader'}
    else:
        params={'type':'reader'}
    if(request.method=='POST'):
        bookid=request.data['books']
        bookid=set(bookid)
        lst=[]
        for book in bookid:
            bk=Festbook.objects.filter(bookid=book).first()
            dic={}
            dic['bookid']=bk.bookid
            dic['name']=bk.name
            dic['author']=bk.author
            dic['price']=bk.price
            lst.append(dic)
        seralizer=Festserializer(lst,many=True)
        return JsonResponse(seralizer.data,safe=False)

def placeorder(request):
    if('reader' in request.session):
        params = {'action': action, 'type': 'reader'}
    else:
        params={'type':'reader'}
    if(request.method=='POST'):
        books=request.POST['order'].split('///')
        books.pop()
        coupon=request.POST['coupon']
        addr=request.POST['address']
        if('oldbook' in request.POST):
            oldbook=1
        else:
            oldbook=0
        if('express' in request.POST):
            express=1
        else:
            express=0
        coupon_valid=False
        used=False
        try:
            code=Referral.objects.get(code=coupon)
            coupon_valid=True
            name=Reader.objects.get(username=code.username)
            if(code.usage<5):
                used=False
                error=f"Your order had been placed. Thank {name.name} for giving coupon"
            else:
                error="Your order had been placed.But the coupon had been used many times"
            code.usage+=1
            code.save()
        except:
            coupon_valid=False
            error="Your order had been placed. However the coupon is incorrect."
        orderid=encrypt(request.session['reader']+str(datetime.now()))
        rdr=Reader.objects.get(username=request.session['reader'])
        for book in books:
            bk=Festorder(userid=rdr,orderId=orderid,bookid=book,coupon=coupon,tme=datetime.now(),status='pending',oldbook=oldbook,express=express,address=addr)
            bk.save()
        fst=Festorder.objects.filter(userid=request.session['reader'])
        fst=list(fst)
        fst=fst[::-1]
        params={'action':action,'type':'reader','Error':error,'fst':fst,'address':rdr.address}
        return render(request,'student/orderrequest.html',params)
            

