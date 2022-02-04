from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api_contracts.views import ContractListAll, ContractCreation, ContractListFilter, ContractDetail
from api_customers.views import CustomerList, CustomerCreation, CustomerFilterList, CustomerDetail
from api_events.views import EventListAll, EventCreation, EventListFilter, EventDetail, CustomerEventList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/login/', TokenObtainPairView.as_view()),
    path('authentication/refresh-token/', TokenRefreshView.as_view()),
    # URI CUSTOMERS
    path('api/customers/', CustomerList.as_view(), name='customer-list'),
    path('api/create-customer/', CustomerCreation.as_view(), name='customer-creation'),
    path('api/customers', CustomerFilterList.as_view(), name='customer-filter-list'),
    path('api/customers/<int:pk>/', CustomerDetail.as_view(), name='customer-update-destroy'),
    # URI CONTRACTS
    path('api/contracts/', ContractListAll.as_view(), name='contracts-list'),
    path('api/create-contract/', ContractCreation.as_view(), name='contract-creation'),
    path('api/contracts', ContractListFilter.as_view(), name='contract-filter-list'),
    path('api/contracts/<int:pk>/', ContractDetail.as_view(), name='contract-update-destroy'),
    # URI CONTRACTS
    path('api/events/', EventListAll.as_view(), name='events-list'),
    path('api/create-event/', EventCreation.as_view(), name='event-creation'),
    path('api/events', EventListFilter.as_view(), name='event-filter-list'),
    path('api/events/<int:pk>/', EventDetail.as_view(), name='event-update-destroy'),
    path('api/event-customer', CustomerEventList.as_view(), name='customer-of-event')

]
