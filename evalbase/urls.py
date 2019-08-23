"""evalbase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from evalbase import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', TemplateView.as_view(template_name='evalbase/signup.html'), name='signup'),

    path('profile/', views.ProfileDetail.as_view(), name='profile'),
    path('profile/create', views.ProfileCreate.as_view(), name='profile-create'),
    path('profile/edit', views.ProfileEdit.as_view(), name='profile-edit'),

    path('org/my-orgs', views.OrganizationList.as_view(), name='my-orgs'),
    path('org/edit/<name>', views.OrganizationEdit.as_view(), name='org-edit'),
    path('org/create', views.OrganizationCreate.as_view(), name='org-create'),
    path('org/join/<key>', views.OrganizationJoin.as_view(), name='org-join'),
    path('org/<str:shortname>', views.OrganizationDetail.as_view(), name='org-detail'),

    path('', TemplateView.as_view(template_name='evalbase/home.html'), name='home'),
]
