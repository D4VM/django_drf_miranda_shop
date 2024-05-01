from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.UserME.as_view()),
    path("", views.UserList.as_view()),
    path("<int:pk>/", views.UserDetail.as_view()),
]
