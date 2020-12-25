from django.urls import path
from librarian import views
urlpatterns = [
    path('', views.home, name='librarian_home'),
    path('login/', views.login, name='librarian_login'),
    path('trackbook/',views.trackbook,name='librarian_trackbook'),
    path('trackstudent/',views.trackstudent,name='librarian_trackstudent'),
    path('return/',views.returnBook,name='returnbook'),
    path('issue',views.issueBook,name='issuebook'),
    path('fake',views.fake,name='fake'),
    path('summary',views.summary,name='summary'),
    path('booklist',views.summary,name='summary'),
    path('print',views.printpage,name='print')
]
