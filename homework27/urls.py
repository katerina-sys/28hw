"""homework27 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ads.views.ad import *
from ads.views.category import *
from homework27 import settings
from users.views import LocationViewSet

router = routers.SimpleRouter()
router.register("location", LocationViewSet)
router.register("ad", AdViewSet)


urlpatterns = [
    path("", root),
    path("admin/", admin.site.urls),
    path('cat/', include('ads.urls.category')),
    path('ad/', include('ads.urls.ad')),
    path('user/', include('users.urls'))
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_url=settings.MEDIA_ROOT)
