"""
URL configuration for djalio project.

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
from django.urls import path
from moods import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Main page
    path('', views.home, name='home'),
    
    # Entry management
    path('add_new_entry/', views.addNewEntry, name='addNewEntry'),
    path('edit_existing_entry/', views.editExistingEntry, name='editExistingEntry'),
    path('remove_existing_entry/', views.removeExistingEntry, name='removeExistingEntry'),
    
    # Activity management
    path('add_new_activity/', views.addNewActivity, name='addNewActivity'),
    path('remove_existing_activity/', views.removeExistingActivity, name='removeExistingActivity'),
    
    # Category management
    path('add_new_category/', views.addNewCategory, name='addNewCategory'),
    path('remove_existing_category/', views.removeExistingCategory, name='removeExistingCategory'),  # New URL
    
    # Mood management
    path('add_new_mood/', views.addNewMood, name='addNewMood'),
]