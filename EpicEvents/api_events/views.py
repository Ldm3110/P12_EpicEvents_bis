from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView

from api_contracts.models import Contracts
from api_customers.models import Customers
from api_customers.permissions import PermissionToAccessCustomer
from api_customers.serializer import CustomerSerializer
from api_events.models import Events
from api_events.permissions import EventPermissions, CustomerInEventPermissions
from api_events.serializer import EventSerializer


class EventListAll(ListAPIView):
    """
    Displays all the Events for all the authenticated users
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    queryset = Events.objects.all()


class EventCreation(CreateAPIView):
    permission_classes = [IsAuthenticated, PermissionToAccessCustomer]

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            contract = Contracts.objects.get(id=serializer.validated_data['contract'].id)
            customer = Customers.objects.filter(id=contract.client_id)
            self.check_object_permissions(self.request, customer)
            contract.status = True
            contract.save()
            serializer.save(sales_contact=self.request.user)
            return Response(
                {"success": "The Event has been successfully created !"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    """
    - Update an event if the user is the support contact or a superuser
    """
    permission_classes = [IsAuthenticated, EventPermissions]

    def patch(self, request, pk):
        event = Events.objects.filter(pk=pk)
        if not event:
            return Response(
                {"error": "This event does not exist !"},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(self.request, event)
        serializer = EventSerializer(event[0], data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "The event has been updated !"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = get_object_or_404(Events, pk=pk)
        self.check_object_permissions(self.request, event)
        event.delete()
        return Response(
            {"success": "Event deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


class EventListFilter(ListAPIView):
    """
    Special class to retrieve an event attached at a customer with following filters :
    - The last name of the customer
    - The email of the customer
    - The date of the event

    This research can be done with one or more filters
    """
    queryset = Events.objects.all()
    filter_fields = ('client__last_name', 'client__email', 'event_date')
    permission_classes = [IsAuthenticated, EventPermissions]
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not queryset:
            return Response(
                {"error": "No events existing - Try with other references"},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(self.request, queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomerEventList(ListAPIView):
    """
    Special class to display the information of a customer attached at an event with following filters :
    - The last name of the customer
    - The email of the customer
    - The date of the event

    This research can be done with one or more filters
    """
    queryset = Events.objects.all()
    filter_fields = ('client__last_name', 'client__email', 'event_date')
    permission_classes = [IsAuthenticated, CustomerInEventPermissions]
    serializer_class = CustomerSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            customer = Customers.objects.filter(id=queryset[0].client_id)
        except IndexError:
            return Response(
                {"error": "No customers existing - Try with other references"},
                status=status.HTTP_404_NOT_FOUND
            )
        self.check_object_permissions(self.request, queryset)
        serializer = self.get_serializer(customer, many=True)
        return Response(serializer.data)
