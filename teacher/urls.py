from django.urls import path
from teacher import views
urlpatterns=[
    path('login/',views.login,name='teacher_login')
]