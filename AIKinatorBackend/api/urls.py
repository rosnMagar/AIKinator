from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.create_session, name="create_session"),
    # path('post/', views.postData),
]
