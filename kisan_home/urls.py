from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('contactus/', views.contact_us, name='contact_us'),
]
