from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api_customers.models import Customers
from api_customers.permissions import PermissionToAccessCustomer
from api_customers.serializer import CustomerSerializer


class CustomerList(ListAPIView):
    """
    Displays all the customers for all the authenticated users
    """
    queryset = Customers.objects.all()
    name = 'customer-list'
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


class CustomerCreation(CreateAPIView):
    """
    Creates a new instance of Customers if user is a member of the 'Sales Team'
    """
    permission_classes = [IsAuthenticated, PermissionToAccessCustomer]

    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            new_customer = serializer.save(sales_contact=self.request.user)
            return Response(
                {"success": f"The Customer named {new_customer} has been successfully created !"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    """
    Updates an instance of Customers if :
    - The User is authenticated
    - The Customer is attached to the User

    To delete an instance of Customer, the user must be a superuser.
    """
    name = 'customer-update-destroy'
    permission_classes = [IsAuthenticated, PermissionToAccessCustomer]

    def patch(self, request, pk):
        customer = get_object_or_404(Customers, pk=pk)
        self.check_object_permissions(self.request, customer)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            customer_updated = serializer.save()
            return Response({"success": f"The Customer {customer_updated} has been updated !"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = get_object_or_404(Customers, pk=pk)
        self.check_object_permissions(self.request, customer)
        customer.delete()
        return Response(f"Customer deleted", status=status.HTTP_204_NO_CONTENT)


class CustomerFilterList(ListAPIView):
    """
    Special class to retrieve a customer with following filters :
    - The last name of the customer
    - The email of the customer

    This research can be done with one or more filters
    """
    queryset = Customers.objects.all()
    filter_fields = ('last_name', 'email',)
    name = 'customer-filter-list'
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, PermissionToAccessCustomer]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        self.check_object_permissions(self.request, queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
