from django.urls import path
from event import views
urlpatterns=[
    path('',views.home,name='event_home'),
    path('view/<str:category>',views.view,name='view'),
    path('getorder',views.getorder,name='getorder'),
    path('placeorder',views.placeorder,name='placeorder')
]