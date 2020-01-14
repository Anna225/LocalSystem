from django.db import models
from cities_light.models import Country, City
from django.contrib.auth.models import AbstractUser 
# Create your models here.

def invoice_file(instance, filename):
    return 'invoice/{1}'.format(instance, filename)

def bank_file(instance, filename):
    return 'bank/{1}'.format(instance, filename)

def content_file_user(instance, filename):
    return 'usercustom/{1}'.format(instance, filename)

def content_file_supplier(instance, filename):
    return 'supplier/{1}'.format(instance, filename)

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

class IVA(models.Model):
    name = models.CharField(max_length=50, blank=True)

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
    iva = models.ForeignKey(IVA, on_delete=models.SET_NULL, blank=True, null=True)
    picture = models.ImageField(upload_to=content_file_supplier, blank=True, null=True)

    def __str__(self):
        return self.name


class Spenses(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=invoice_file, blank=True, null=True)
    iva = models.ForeignKey(IVA, on_delete=models.SET_NULL, blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.amount

class User(AbstractUser):
    picture = models.ImageField(upload_to=content_file_user, blank=True)
    telephone = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)    
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Company, related_name='user_relationship',on_delete=models.SET_NULL, blank=True, null=True)
    movil = models.CharField(max_length=30, blank=True, null=True)
    wechat = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        permissions = (("admin_user","Can use modules admin"),("guest_user","Can use modules guest"))

class Bank(models.Model):
    supplier_name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(null=True, blank=True)
    invoice_name = models.FileField(upload_to=bank_file, blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    bank_search_start = models.DateField(null=True, blank=True)
    bank_search_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.supplier_name

class BankData(models.Model):
    date_first = models.DateField(null=True, blank=True)
    paid_name = models.CharField(max_length=100, blank=True, null=True)
    bank_num = models.ForeignKey(Bank, on_delete=models.SET_NULL, blank=True, null=True)
    date_second = models.DateField(null=True, blank=True)
    amount = models.CharField(max_length=30, blank=True, null=True)
    balance = models.CharField(max_length=30, blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.paid_name


