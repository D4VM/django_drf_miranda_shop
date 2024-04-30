from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListCreateAPIVIEW.as_view()),
    path('<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view()),

]