"""
URL configuration for warzone_tools project.

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
from django.urls import include, path


from .import views

app_name = 'eve_tools'

urlpatterns = [
    path("index/", views.index, name="index"),
    path('tracker/<str:faction>/', views.tracker, name='battlefields_tracker'),
    path('battlefield/<int:battlefield_id>/', views.battlefield_detail, name='battlefield_detail'),
    path('system/<int:solarsystem_id>/', views.system_detail, name='system_detail'),
    path('report-battlefield/', views.report_battlefield, name='report_battlefield'),
]