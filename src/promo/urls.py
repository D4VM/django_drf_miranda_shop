from django.urls import path
from . import views

urlpatterns = [
    path("", views.promo_list),
    path("<int:pk>/", views.promo_details),
]
