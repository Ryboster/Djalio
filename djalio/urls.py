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
from Controllers.Diaries import Diary
from moods import media_manager as MediaManager
from django.conf import settings
from django.conf.urls.static import static

diary = Diary()

urlpatterns = [
    
    path('upload-media/', MediaManager.UploadMedia, name='upload_media'),
    
    path("", views.home, name="home"),
    
    path("create_new/", views.CreateNew, name="createNew"),
    
    ### Main page
    #path('', views.home, name='home'),    
    ### DIARY section
    path("Diary/<int:diary_id>/", diary.RenderDiary, name="ViewDiary"),
    path("Diary/<int:diary_id>/remove", diary.RemoveDiary, name="RemoveDiary"),
    
        ## Entry management
    path('Diary/<int:diary_id>/add_new_entry/', diary.AddNewEntryToDiary, name='addNewEntry'),
    path('Diary/<int:diary_id>/edit_existing_entry/', diary.editExistingEntry, name='editExistingEntry'),
    path('Diary/<int:diary_id>/remove_existing_entry/', diary.removeExistingEntry, name='removeExistingEntry'),
    
        ## Activity management
    path('Diary/<int:diary_id>/add_new_activity/', diary.addNewActivity, name='addNewActivity'),
    path("Diary/<int:diary_id>/edit_activity/", diary.editActivity, name="editActivity"),
    path('Diary/<int:diary_id>/remove_existing_activity/', diary.removeExistingActivity, name='removeExistingActivity'),
    
        ## Category management
    path('Diary/<int:diary_id>/add_new_category/', diary.addNewCategory, name='addNewCategory'),
    path('Diary/<int:diary_id>/edit_category/', diary.editCategory, name='editCategory'),
    path('Diary/<int:diary_id>/remove_existing_category/', diary.removeExistingCategory, name='removeExistingCategory'),  # New URL
    
        ## Mood management    
    path('Diary/<int:diary_id>/add_new_mood/', diary.addNewMoodToDiary, name='addNewMood'),
    path('Diary/<int:diary_id>/edit_mood/', diary.EditMood, name='editMood'),
    path('Diary/<int:diary_id>/remove_mood/', diary.RemoveMood, name='removeMood')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)