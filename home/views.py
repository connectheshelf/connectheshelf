from django.shortcuts import render,redirect

# Create your views here.
def home(request):
    if('reader' in request.session):
        action=[{"name":"view books","link":""},{"name":"profile","link":"profile"},{"name":"request","link":"request"},{"name":"orders and requests","link":"view_order"}]
        tp="reader"
    elif('librarian' in request.session):
        action = [
            {"name": "issue a book", "link": "issue"},
            {"name": "return a book", "link": "return"},
            {"name": "track book record", "link": "trackbook"},
            {"name": "track student record", "link": "trackstudent"},
            {"name": "get summary", "link": "summary"},
            # {"name": "manage book list", "link": "booklist"},
        ]
        tp="librarian"
    else:
        action=None
        tp=None
    params={"action":action,"type":tp}
    return render(request,'index.html',params)

def logout(request):
    if('librarian' in request.session):
        del request.session['librarian']
    if('teacher' in request.session):
        del request.session['teacher']
    if('reader' in request.session):
        del request.session['reader']
    if('school' in request.session):
        del request.session['school']
    return redirect('home')

def donation(request):
    if(request.method=='GET'):
        return render(request,'donation.html')
    if(request.method=='POST'):
        return redirect('donation')