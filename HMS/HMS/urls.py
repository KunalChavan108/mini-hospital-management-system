"""
URL configuration for HMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from hospital import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index),
    path('doc_signup/',views.doc_signup),
    path('pat_signup/',views.pat_signup),
    path('pat_login/',views.pat_login),
    path('pat_dash/',views.pat_dash),
    path('view_doctors/',views.view_doctors),
    path('book/<int:doc_id>/',views.book_appointment),
    path('my_appointments/',views.my_appointments),
    path('doc_login/',views.doc_login),
    path('doc_dash/',views.doc_dash)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

