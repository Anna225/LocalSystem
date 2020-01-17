from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from System.part.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from System.part.models import Company, Supplier, Spenses, IVA, Bank, BankData, Category
from cities_light.models import Country
import os

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from System.part.forms import CompanyForm, SupplierForm, SpensesForm, UserForm, BankForm, CategoryForm

from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, RedirectView

import pandas as pd
from django.db.models import Sum, Count

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
        spenses = Spenses.objects.filter(user_id=self.request.user.pk).count()
        category = Category.objects.all().count()
        bank = Bank.objects.filter(user_id=self.request.user.pk).count()

        context["company_num"] = company
        context["supplier_num"] = supplier
        context["spense_num"] = spenses
        context["empty"] = Spenses.objects.filter(user_id=self.request.user.pk).exclude(file__exact="").count()
        context['category_num'] = category
        context['bank_num'] = bank
        
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
    #if request.user.is_staff == True:
       # spenses = Spenses.objects.all().order_by('date')
    #else:
    spenses = Spenses.objects.filter(user_id=request.user.id).order_by('date')
    
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
        category = Category.objects.all()
        iva = IVA.objects.all()

        context["companys"] = company
        context["suppliers"] = supplier
        context["categorys"] = category
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

@method_decorator(login_required, name='dispatch')
class category(ListView):
    model = Category
    fields = "__all__"
    template_name = "category/Categorie.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorys'] = Category.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class categoryadd(CreateView):
    model = Category
    fields = "__all__"
    template_name = "category/categoryadd.html"
    success_url = reverse_lazy('category')

def delete_category(request):
    my_id = request.POST.get('value')
    category = Category.objects.get(id=my_id)
    category.delete()
    return HttpResponse('Ok')

@method_decorator(login_required, name='dispatch')
class categoryupdate(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "category/update_category.html"
    success_url = reverse_lazy('category')

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
        bank = Bank.objects.filter(user_id=self.request.user.pk).order_by('date')
        paginator = Paginator(bank, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context["banks"] = page_obj

        return context

@method_decorator(login_required, name='dispatch')
class bankupdate(UpdateView):
    
    model = Bank
    form_class = BankForm
    template_name = "bank/bank_update.html"
    success_url = reverse_lazy('banklist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file'] = Bank.objects.get(pk=self.kwargs.get('pk'))
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
    invoice_data = pd.read_csv(bank.invoice_name)
    
    temp = [[]]
    temp.clear()
    for i in range(len(invoice_data)):
        array = []
        for j in range(len(invoice_data.loc[i])):
            array.append((invoice_data.loc[i])[j])
        temp.append(array)
    
    if len(temp) > 0:
        for i in range(2, len(temp)):
            
            temp_fecha = temp[i][0].split('/')[2] + "-" + temp[i][0].split('/')[1] + "-" + temp[i][0].split('/')[0]
            temp_fecha_vlaor = temp[i][2].split('/')[2] + "-" + temp[i][2].split('/')[1] + "-" + temp[i][2].split('/')[0]

            bankdata = BankData(
                date_first = temp_fecha,
                paid_name = temp[i][1],
                bank_num_id = my_id,
                date_second=temp_fecha_vlaor,
                amount=temp[i][3],
                balance=temp[i][4],
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
        context['bankdatas'] = BankData.objects.filter(bank_num_id=self.kwargs.get('pk'), amount__lt=0).order_by('date_first')
        bank_date = Bank.objects.get(pk=self.kwargs.get('pk'))
        context['value'] = self.kwargs.get('pk')
        context['spenses'] = Spenses.objects.filter(user_id=self.request.user.pk, amount__lt=0).filter(date__gte=bank_date.bank_search_start, date__lte=bank_date.bank_search_end).order_by('date')
        #context['spenses_all'] = Spenses.objects.filter(date__gte=bank_date.bank_search_start, date__lte=bank_date.bank_search_end).order_by('date').count()
        #context['bankdatas_all'] = BankData.objects.filter(bank_num_id=self.kwargs.get('pk')).order_by('date_first').count()
        bank_except = BankData.objects.filter(bank_num_id=self.kwargs.get('pk')).exclude(amount__in=Spenses.objects.filter(date__gte=bank_date.bank_search_start, date__lte=bank_date.bank_search_end, user_id=self.request.user.pk).values_list('amount', flat=True), date_first__in=Spenses.objects.filter(date__gte=bank_date.bank_search_start, date__lte=bank_date.bank_search_end, user_id=self.request.user.pk).values_list('date', flat=True)).all()

        for bank_date_temp in BankData.objects.filter(bank_num_id=self.kwargs.get('pk')):
            bank_date_temp.flag = False
            bank_date_temp.save()

        if bank_except.count() != 0:
            for bank_except_detail in bank_except:
                bank_except_detail.flag = True
                bank_except_detail.save()
                
        spenses_except = Spenses.objects.exclude(amount__in=BankData.objects.filter(bank_num_id=self.kwargs.get('pk'), amount__lt=0).values_list('amount', flat=True),date__in=BankData.objects.filter(bank_num_id=self.kwargs.get('pk'), amount__lt=0).values_list('date_first', flat=True)).all()
        
        if spenses_except.count() != 0:
            for spenses_except_detail in spenses_except:
                spenses_except_detail.flag = True
                spenses_except_detail.save()
        else:
            spenses_temp = Spenses.objects.filter(date__gte=bank_date.bank_search_start, date__lte=bank_date.bank_search_end).order_by('date')
            for temp_spense in spenses_temp:
                temp_spense.flag = False
                temp_spense.save()

        return context

    def post(self, request, *args, **kwargs):
     
        if request.method == 'POST':
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            value = request.POST.get('value')
            spenses = Spenses.objects.filter(user_id=self.request.user.pk, date__gte=start_date, date__lte=end_date).order_by('date')

            return render(request, 'bank/banksearch.html', {'spenses': spenses, 'start_date': start_date, 'end_date': end_date, 'value':value}) 
 

def delete_bank(request):
    my_id = request.POST.get('value')
    bankdata = BankData.objects.filter(bank_num_id=my_id)
    for data in bankdata:
        data.delete()
    bank = Bank.objects.get(id=my_id)
    bank.delete()
    return HttpResponse('Ok')

@method_decorator(login_required, name='dispatch')
class statistic(TemplateView):
    
    model = Spenses
    fields = "__all__"
    template_name = "statistic/statistic.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics_spense = Spenses.objects.filter(user_id=self.request.user.pk, amount__lt=0).count()
        #print("===============", self.request.user.pk)
        if statistics_spense != 0:

            statis = Spenses.objects.filter(user_id=self.request.user.pk, amount__lt=0).exclude(category_id__isnull=True).values('category').annotate(dsum=Sum('amount')).order_by('-dsum')
            array = [[]]
            array.clear()
            head = ['Category', 'Sum']
            array.append(head)
            sum = 0
            for stat in statis:
                temp = []
                category_name = Category.objects.get(pk=stat['category'])
                temp.append(str(category_name))
                temp.append(abs(stat['dsum']))
                array.append(temp)
                sum += abs(stat['dsum'])

            context["statistics_spenses"] = array
            context["sum"] = sum

            statistic_invoice = Spenses.objects.filter(user_id=self.request.user.pk, amount__lt=0).exclude(file__exact="").count()
            statistic_invoice_empty = Spenses.objects.filter(user_id=self.request.user.pk, amount__lt=0, file__exact="").count()
            invoice_head = ["Invoice", "Count"]
            invoice_temp = []
            invoice_temp.append("Factura")
            invoice_temp.append(statistic_invoice)
            
            invoice_array = [[]]
            invoice_array.clear()
            invoice_array.append(invoice_head)
            invoice_array.append(invoice_temp)
            invoice_temper = []
            invoice_temper.append("Vacío")
            invoice_temper.append(statistic_invoice_empty)
            invoice_array.append(invoice_temper)
            context["invoice"] = invoice_array
        else:
            array = [[]]
            sum = 0
            invoice_array = [[]]
            context["statistics_spenses"] = array
            context["sum"] = sum
            context["invoice"] = invoice_array

        statistic_tax = Spenses.objects.filter(user_id=self.request.user.pk, amount__lt=0).count()
        if statistic_tax != 0:

            statis = Spenses.objects.filter(user_id=self.request.user.pk, amount__lt=0).exclude(category_id__isnull=True).values('iva').annotate(dsum=Sum('amount')).order_by('-dsum')
            array = [[]]
            array.clear()
            head = ['IVA', 'Sum']
            array.append(head)
            for stat in statis:
                temp = []
                iva_name = IVA.objects.get(pk=stat['iva'])
                temp.append(str(iva_name))
                temp.append(abs(stat['dsum']))
                array.append(temp)

            context["statistic_taxs"] = array

        else:
            array = [[]]
            context["statistic_taxs"] = array
        
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            start = request.POST.get('start_date')
            end = request.POST.get('end_date')

            statistic = Spenses.objects.filter(date__gte=start, date__lte=end).count()
            if statistic != 0:
                statis = Spenses.objects.filter(date__gte=start, date__lte=end).values('category').annotate(dsum=Sum('amount')).order_by('-dsum')
                array = [[]]
                array.clear()
                head = ['Category', 'Sum']
                array.append(head)
                for stat in statis:
                    temp = []
                    category_name = Category.objects.get(pk=stat['category'])
                    temp.append(str(category_name))
                    temp.append(abs(stat['dsum']))
                    array.append(temp)

                return render(request, 'statistic/statistic.html', {'statistics': array, 'start':start, 'end':end})

            else:
                array = [[]]
                return render(request, 'statistic/statistic.html', {'statistics': array,'start':start, 'end':end})


    
