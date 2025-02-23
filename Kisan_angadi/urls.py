"""
URL configuration for Kisan_angadi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.models import User


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kisan_home.urls')),
    path('Shop/', include('Shop.urls')),
    path("blog/", include("blog.urls")), 
    path('', include('About.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)


def create_superuser(request):
    username = "admin"
    email = "admin@example.com"
    password = "yourpassword"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        return HttpResponse("Superuser created successfully! 🎉")
    else:
        return HttpResponse("Superuser already exists!")

urlpatterns += [
    path("create-admin/", create_superuser),  # Temporary route
]
