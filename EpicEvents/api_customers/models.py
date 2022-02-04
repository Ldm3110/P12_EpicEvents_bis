from django.db import models

from api_users.models import Employees


class Customers(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True, null=False, max_length=100)
    phone = models.CharField(max_length=10, blank=True)
    mobile = models.CharField(max_length=10, blank=True)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    # Link with the seller's contact
    sales_contact = models.ForeignKey(Employees, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Customers'
        verbose_name_plural = 'Customers'

    def __repr__(self):
        return "%s %s - %s" % (self.first_name, self.last_name, self.company_name)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
