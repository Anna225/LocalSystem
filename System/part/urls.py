from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from System.part import views as part_view
from .views import companyadd, supplieradd, spensesadd, userlist, index
from .views import companyupdate, supplierupdate, spensesupdate

from django.contrib.auth.views import PasswordResetView 
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [

    path('', part_view.home, name='home' ),
    path('login/', auth_views.LoginView.as_view(template_name = 'login_page.html'), name='login'),
    path('logout_delete', part_view.deleteDirectory, name='logout_delete'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login_page.html'), name='logout'),
    path('signup/', part_view.register, name='signup'),
    url(r'^index/$', index.as_view(), name='index'),
    url(r'^companyaddindex/$', companyadd.as_view(), name='companyadd'),
    url(r'^companyupdateindex/(?P<pk>\d+)/$', companyupdate.as_view(), name='companyupdate'),
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
    #url(r'^useradd/$', useradd.as_view(), name='useradd'),
    url(r'^delete_user/$', part_view.delete_user, name='delete_user'),
    url(r'^reset/password/$', PasswordResetView.as_view(template_name='password_reset_form.html', email_template_name='password_reset_email.html'), name='password_reset'),
    url(r'^reset/password/reset/done/$', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    url(r'^change/password/(?P<pk>[0-9]+)/$', PasswordChangeView.as_view(template_name='password_change.html', success_url='/'), name='change_password'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)