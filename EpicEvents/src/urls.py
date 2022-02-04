from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api_customers.views import CustomerList, CustomerCreation, CustomerFilterList, CustomerDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/login/', TokenObtainPairView.as_view()),
    path('authentication/refresh-token/', TokenRefreshView.as_view()),
    # URI CUSTOMERS
    path('api/customers/', CustomerList.as_view(), name='customer-list'),
    path('api/create-customer/', CustomerCreation.as_view(), name='customer-creation'),
    path('api/customers', CustomerFilterList.as_view(), name='customer-filter-list'),
    path('api/customers/<int:pk>/', CustomerDetail.as_view(), name='customer-update-destroy'),
]
