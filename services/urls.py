from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import read_song_service, create_song_service, update_song_service, delete_song_service


urlpatterns = [
    
    path('read/', csrf_exempt(read_song_service.read_song)),
    path('create/', csrf_exempt(create_song_service.create_song)),
    path('update/', csrf_exempt(update_song_service.update_song)),
    path('delete/', csrf_exempt(delete_song_service.delete_song)),
]

