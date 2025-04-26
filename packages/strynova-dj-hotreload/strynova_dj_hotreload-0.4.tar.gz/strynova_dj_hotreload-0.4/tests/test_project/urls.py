"""
URL Configuration for test_project.
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render

# A simple view to test the server
def home(request):
    return render(request, 'base.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]
