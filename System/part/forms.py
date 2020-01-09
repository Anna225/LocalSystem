from django import forms
from System.part.models import Company, Supplier, Spenses
from cities_light.models import Country
from System.part.models import User

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        country_company = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
        fields = (
            'name', 
            'phone',
            'address',
            'web',
            'nif',
            'description',
            'country_company'
        )
        widgets = {
            'name': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'name', 'id':'name', 'required':True}),
            'phone': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'phone', 'id':'phone', 'required':True}),
            'address': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'address', 'id':'address', 'required':True}),
            'web': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'web', 'id':'web', 'required':True}),
            'nif': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'nif', 'id':'nif', 'required':True}),
            
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        country_supplier = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
        fields = (
            'name', 
            'phone',
            'address',
            'web',
            'nif',
            'description',
            'country_supplier',
            'iva'
        )
        widgets = {
            'name': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'name', 'id':'name', 'required':True}),
            'phone': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'phone', 'id':'phone', 'required':True}),
            'address': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'address', 'id':'address', 'required':True}),
            'web': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'web', 'id':'web', 'required':True}),
            'nif': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'nif', 'id':'nif', 'required':True}),
            
        }

class SpensesForm(forms.ModelForm):
    class Meta:
        model = Spenses
        fields = ('amount', 'date', 'company', 'supplier', 'file', 'iva')
        widgets = {
            'amount': forms.TextInput(attrs={'type':'text', 'class':'form-control', 'name':'amount', 'id':'amount', 'required':True}),
            'file': forms.FileInput(attrs={'class':'custom-file-input'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
        company = forms.ModelChoiceField(queryset=Company.objects.all(), required='true')
        fields = ('username', 'first_name', 'last_name', 'picture', 'country', 'email', 'company', 'telephone', 'movil')
        widgets = {
            'picture': forms.FileInput(attrs={'class':'custom-file-input','onchange':'readURL(this);'})
        }