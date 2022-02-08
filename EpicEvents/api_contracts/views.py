from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api_contracts.models import Contracts
from api_contracts.serializer import ContractSerializer
from api_customers.models import Customers
from api_customers.permissions import PermissionToAccessCustomer


class ContractListAll(ListAPIView):
    """
    Displays all the contracts for all the authenticated users
    """
    serializer_class = ContractSerializer
    queryset = Contracts.objects.all()
    permission_classes = [IsAuthenticated]


class ContractCreation(CreateAPIView):
    """
    Creates a new instance of 'Contracts' if :
    - The user is a member of 'Sales Team'
    - The customer is attached to the User
    """
    permission_classes = [IsAuthenticated, PermissionToAccessCustomer]

    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            customer = Customers.objects.filter(id=serializer.validated_data['client'].id)
            self.check_object_permissions(self.request, customer)
            serializer.save(sales_contact=self.request.user)
            return Response(
                {"success": "The Contract has been successfully created !"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractListFilter(ListAPIView):
    """
    Special class to retrieve a contract attached at a customer with following filters :
    - The last name of the customer
    - The email of the customer
    - The date of creation of the contract
    - The amount of this contract

    This research can be done with one or more filters
    """
    queryset = Contracts.objects.all()
    filter_fields = ('client__last_name', 'client__email', 'date_created', 'amount')
    permission_classes = [IsAuthenticated, PermissionToAccessCustomer]
    serializer_class = ContractSerializer
    name = 'contract-filter-list'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)
        try:
            customer = Customers.objects.filter(id=queryset[0].client_id)
        except IndexError:
            return Response(
                {"error": "No existing contracts - Try with other references"},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(self.request, customer)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ContractDetail(APIView):
    """
    - Update a contract if the user is the creator of it or a superuser
    - Delete a contract (only for superuser)
    """
    permission_classes = [IsAuthenticated, PermissionToAccessCustomer]

    def patch(self, request, pk):
        contract = get_object_or_404(Contracts, pk=pk)
        customer = Customers.objects.get(id=contract.client_id)
        self.check_object_permissions(self.request, customer)
        serializer = ContractSerializer(contract, data=request.data, partial=True)
        if serializer.is_valid():
            contract_updated = serializer.save()
            return Response({"success": f"The contract of {contract_updated.client} has been updated !"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contract = get_object_or_404(Contracts, pk=pk)
        customer = Customers.objects.get(id=contract.client_id)
        self.check_object_permissions(self.request, customer)
        customer.delete()
        return Response("Customer deleted", status=status.HTTP_204_NO_CONTENT)
