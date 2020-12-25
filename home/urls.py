from django.urls import path
from home import views

urlpatterns=[
    path('',views.home,name="home"),
    path('logout/',views.logout,name="logout"),
    path('donation/',views.donation,name='donation')
]