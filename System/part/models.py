from django.db import models
from cities_light.models import Country
# Create your models here.

def invoice_file(instance, filename):
    return 'invoice/{1}'.format(instance, filename)

class Company(models.Model):
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    address = models.TextField(blank=True)
    web = models.CharField(max_length=50, blank=True)
    nif = models.CharField(max_length=50, blank=True)
    country_company = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    address = models.TextField(blank=True)
    web = models.CharField(max_length=50, blank=True)
    nif = models.CharField(max_length=50, blank=True)
    country_supplier = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Spenses(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=invoice_file, blank=True, null=True)

    def __str__(self):
        return self.amount
