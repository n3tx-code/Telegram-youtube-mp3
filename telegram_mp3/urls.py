from django.urls import path


from mp3 import views as mp3Views

urlpatterns = [
    path("mp3", mp3Views.messageFromTelegram, name="enter"),
]
