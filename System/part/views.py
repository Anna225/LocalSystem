from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from System.part.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from System.part.models import Company, Supplier, Spenses, IVA, Bank, BankData
from cities_light.models import Country
import os

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from System.part.forms import CompanyForm, SupplierForm, SpensesForm, UserForm

from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, RedirectView

import pandas as pd

# Create your views here.

def home(request):
    return redirect('login')

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "login_page.html"
    
    def get_success_url(self):
        return reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)

class LogoutView(RedirectView):
    url = '/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

# Register Function
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        cpassword = request.POST.get('password2')
        email_qs = User.objects.filter(email = email)
        if email_qs.exists():
            return render(request, 'register.html', {'error': 'Ya existe el correo electrónico.'})
        if password != cpassword:
            return render(request, 'register.html', {'error': "Los dos campos de contraseña no coinciden.", 'username':username, 'email':email})
        if len(password)<6:
            return render(request, 'register.html', {'error': "La contraseña debe tener más de 6 caracteres", 'username':username, 'email':email})
        password = make_password(password)
        user = User(
            email = email,
            username = username,
            first_name=firstname,
            last_name=lastname,
            password = password
        )
        user.save()
        #login(request, user)
        return redirect('login')

    else:
        form = UserCreationForm()
        return render(request, 'register.html',{'form':form})

@method_decorator(login_required, name='dispatch')
class index(ListView):
    model = Company
    fields = "__all__"
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        company = Company.objects.all().count()
        supplier = Supplier.objects.all().count()
        
        context["company_num"] = company
        context["supplier_num"] = supplier
        
        return context

@method_decorator(login_required, name='dispatch')
class companylist(ListView):
    model = Company
    fields = "__all__"
    template_name = "company/index.html"

    def get_context_data(self, **kwargs):
        context = super(companylist, self).get_context_data(**kwargs)
        company = Company.objects.all().order_by('name')
        paginator = Paginator(company, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context["companies"] = page_obj

        return context

def delete_company(request):
    my_id = request.POST.get('value')
    company = Company.objects.get(id=my_id)
    company.delete()
    return HttpResponse('Ok')

@method_decorator(login_required, name='dispatch')
class companyadd(CreateView):
    
    model = Company
    fields = "__all__"
    template_name = "company/companyadd.html"
    def get_context_data(self, **kwargs):
        context = super(companyadd, self).get_context_data(**kwargs)
        country = Country.objects.all()
        context["countrys"] = country
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            web = request.POST.get('web')
            nif = request.POST.get('nif')
            countries = request.POST.get('country')
            description = request.POST.get('description')
            company = Company(
                name = name,
                phone = phone,
                address = address,
                web=web,
                nif=nif,
                country_company_id=countries,
                description=description,
            )
            company.save()
        
        return redirect('companylist')

@method_decorator(login_required, name='dispatch')
class companyupdate(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "company/update_company.html"
    success_url = reverse_lazy('companylist')

@login_required
def supplier(request):
    supplier_data = Supplier.objects.all().order_by('name')
    page = request.GET.get('page', 1)
    paginator = Paginator(supplier_data, 10)
    try:
        supplier = paginator.page(page)
    except PageNotAnInteger:
        supplier = paginator.page(1)
    except EmptyPage:
        supplier = paginator.page(paginator.num_pages)
    return render(request, 'supplier/supplier.html', {'suppliers':supplier})

def delete_supplier(request):
    my_id = request.POST.get('value')
    supplier = Supplier.objects.get(id=my_id)
    supplier.delete()
    return HttpResponse('Ok')

@method_decorator(login_required, name='dispatch')
class userlist(ListView):
    model = User
    fields = "__all__"
    template_name = "userslist.html"

    def get_context_data(self, **kwargs):
        context = super(userlist, self).get_context_data(**kwargs)
        users = User.objects.all()
        context['users'] = users
        
        return context

def delete_user(request):
    my_id = request.POST.get('value')
    user = User.objects.get(id=my_id)
    user.delete()
    return HttpResponse('Ok')

def detect_new_user(request):
    my_id = request.POST.get('value')
    user = User.objects.get(id=my_id)
    user.flag = True
    user.save()
    return HttpResponse('Ok')

@method_decorator(login_required, name='dispatch')
class supplieradd(CreateView):
    model = Supplier
    fields = "__all__"
    template_name = "supplier/supplieradd.html"
    success_url = reverse_lazy('supplier')

    def get_context_data(self, **kwargs):
        context = super(supplieradd, self).get_context_data(**kwargs)
        country = Country.objects.all()
        iva = IVA.objects.all()
        context["countrys"] = country
        context["ivas"] = iva
        return context
    '''
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            web = request.POST.get('web')
            nif = request.POST.get('nif')
            countries = request.POST.get('country')
            description = request.POST.get('description')
            iva = request.POST.get('iva')
            supplier = Supplier(
                name = name,
                phone = phone,
                address = address,
                web=web,
                nif=nif,
                country_supplier_id=countries,
                description=description,
                iva_id=iva,
            )
            supplier.save()
        
        return redirect('supplier')
    '''
@method_decorator(login_required, name='dispatch')
class supplierupdate(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "supplier/update_supplier.html"
    success_url = reverse_lazy('supplier')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier'] = Supplier.objects.get(pk=self.kwargs.get('pk'))
        return context

@login_required
def spenses(request):
    spenses = Spenses.objects.all().order_by('date')
    page = request.GET.get('page', 1)
    paginator = Paginator(spenses, 10)
    try:
        spense_page = paginator.page(page)
    except PageNotAnInteger:
        spense_page = paginator.page(1)
    except EmptyPage:
        spense_page = paginator.page(paginator.num_pages)
    return render(request, 'spenses/spenses.html', {'spense_page':spense_page})

def delete_spense(request):
    my_id = request.POST.get('value')
    spenses = Spenses.objects.get(id=my_id)
    spenses.delete()
    return HttpResponse('Ok')

@method_decorator(login_required, name='dispatch')
class spensesadd(CreateView):
    model = Spenses
    fields = '__all__' 
    template_name = "spenses/spenseadd.html"
    success_url = reverse_lazy('spenses')

    def get_context_data(self, **kwargs):
        context = super(spensesadd, self).get_context_data(**kwargs)
        company = Company.objects.all()
        supplier = Supplier.objects.all()
        iva = IVA.objects.all()

        context["companys"] = company
        context["suppliers"] = supplier
        context["ivas"] = iva
        return context

@method_decorator(login_required, name='dispatch')
class spensesupdate(UpdateView):
    model = Spenses
    form_class = SpensesForm
    template_name = "spenses/spensesupdate.html"
    success_url = reverse_lazy('spenses')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = Spenses.objects.get(pk=self.kwargs.get('pk'))
        return context

@login_required
def Categorie(request):
    country = Country.objects.all()
    return render(request, 'category/Categorie.html', {'country':country})

@method_decorator(login_required, name='dispatch')
class userinformation(ListView):
    model = User
    fields = '__all__'
    template_name = "personal/personallist.html"
    success_url = reverse_lazy('userinformation_update')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        return context

@method_decorator(login_required, name='dispatch')
class userinformation_update(UpdateView):
    
    model = User
    form_class = UserForm
    template_name = "personal/personallist_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse('userinformation', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class banklist(ListView):
    
    model = Bank
    fields = "__all__"
    template_name = "bank/banklist.html"

    def get_context_data(self, **kwargs):
        context = super(banklist, self).get_context_data(**kwargs)
        bank = Bank.objects.all().order_by('date')
        paginator = Paginator(bank, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context["banks"] = page_obj

        return context

@method_decorator(login_required, name='dispatch')
class bankadd(CreateView):
    
    model = Bank
    fields = "__all__"
    template_name = "bank/bankadd.html"
    success_url = reverse_lazy('banklist')


def add_bank_flag(request):
    my_id = request.POST.get('value')
    bank = Bank.objects.get(id=my_id)
    bank.flag = True
    bank.save()
    invoice_data = pd.read_excel(bank.invoice_name)

    temp = [[]]
    temp.clear()
    for i in range(len(invoice_data)):
        array = []
        for j in range(len(invoice_data.loc[i])):
            array.append((invoice_data.loc[i])[j])
        temp.append(array)
    if len(temp) > 0:
        for i in range(len(temp)):
            bankdata = BankData(
                date_first = temp[i][0],
                paid_name = temp[i][1],
                bank_num_id = my_id,
                date_second=temp[i][2],
                amount=temp[i][3],
            )
            bankdata.save()

    return HttpResponse('Ok')

@method_decorator(login_required, name='dispatch')
class bankdetail(ListView):
    
    model = BankData
    fields = "__all__"
    template_name = "bank/bankdetail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bankdatas'] = BankData.objects.filter(bank_num_id=self.kwargs.get('pk')).order_by('date_first')
        context['spenses'] = Spenses.objects.all().order_by('date')
        return context
    

def delete_bank(request):
    my_id = request.POST.get('value')
    bankdata = BankData.objects.filter(bank_num_id=my_id)
    for data in bankdata:
        data.delete()
    bank = Bank.objects.get(id=my_id)
    bank.delete()
    return HttpResponse('Ok')