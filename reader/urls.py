from django.urls import path
from reader import views
urlpatterns = [
    path('', views.home, name='reader_home'),
    path('login/', views.login, name='reader_login'),
    path('signup',views.signup,name='reader_signup'),
    path('verify',views.verify,name='reader_verify'),
    path('fetchbook',views.fetchbook,name='fetchbook'),
    path('order/',views.order,name='order'),
    path('getstock/',views.getstock,name='stock'),
    path('view_order',views.viewOrder,name='view_order'),
    path('profile',views.profile,name='profile'),
    path('request',views.requestt,name='request')
]
