from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from System.part import views as part_view
from .views import companyadd, supplieradd, spensesadd, userlist, index, userinformation, userinformation_update, companylist, banklist, bankadd, bankdetail
from .views import companyupdate, supplierupdate, spensesupdate

from django.contrib.auth.views import PasswordResetView 
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView

from .views import LoginView
from .views import LogoutView

urlpatterns = [

    path('', part_view.home, name='home' ),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    path('signup/', part_view.register, name='signup'),
    url(r'^index/$', index.as_view(), name='index'),
    url(r'^companylist/$', companylist.as_view(), name='companylist'),
    url(r'^companyadd/$', companyadd.as_view(), name='companyadd'),
    url(r'^companyupdate/(?P<pk>\d+)/$', companyupdate.as_view(), name='companyupdate'),
    url(r'^delete_company/$', part_view.delete_company, name='delete_company'),
    path('supplier/', part_view.supplier, name='supplier'),
    url(r'^supplieradd/$', supplieradd.as_view(), name='supplieradd'),
    url(r'^supplierupdate/(?P<pk>\d+)/$', supplierupdate.as_view(), name='supplierupdate'),
    url(r'^delete_supplier/$', part_view.delete_supplier, name='delete_supplier'),
    path('spenses/', part_view.spenses, name='spenses'),
    url(r'^spensesadd/$', spensesadd.as_view(), name='spensesadd'),
    url(r'^spensesupdate/(?P<pk>\d+)/$', spensesupdate.as_view(), name='spensesupdate'),
    url(r'^delete_spense/$', part_view.delete_spense, name='delete_spense'),
    path('Categorie/', part_view.Categorie, name='Categorie'),
    url(r'^userlist/$', userlist.as_view(), name='userlist'),
    url(r'^delete_user/$', part_view.delete_user, name='delete_user'),
    url(r'^detect_new_user/$', part_view.detect_new_user, name='detect_new_user'),
    url(r'^reset/password/$', PasswordResetView.as_view(template_name='password_reset_form.html', email_template_name='password_reset_email.html'), name='password_reset'),
    url(r'^reset/password/reset/done/$', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    url(r'^change/password/(?P<pk>[0-9]+)/$', PasswordChangeView.as_view(template_name='password_change.html', success_url='/'), name='change_password'),
    url(r'^personallist/(?P<pk>\d+)/$', userinformation.as_view(), name='userinformation'),
    url(r'^personallist_update/(?P<pk>\d+)/$', userinformation_update.as_view(), name='userinformation_update'),
    url(r'^banklist/$', banklist.as_view(), name='banklist'),
    url(r'^bankadd/$', bankadd.as_view(), name='bankadd'),
    url(r'^bankdetail/(?P<pk>\d+)$', bankdetail.as_view(), name='bankdetail'),
    url(r'^add_bank_flag/$', part_view.add_bank_flag, name='add_bank_flag'),
    url(r'^delete_bank/$', part_view.delete_bank, name='delete_bank'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)