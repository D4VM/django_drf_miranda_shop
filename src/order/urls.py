from django.urls import path
from .views import order_list, order_detail
from .invoice import order_invoice

urlpatterns = [
    path("", order_list),
    path("<int:pk>/invoice/", order_invoice),
    path("<int:pk>/", order_detail),
]
