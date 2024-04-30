from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListCreateAPIView.as_view()),
    path('edit/<int:pk>/', views.OrderUpdateAPIView.as_view()),
    path('delete/<int:pk>/', views.OrderDestroyAPIView.as_view()),
]