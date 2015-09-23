"""proto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from .views import UserActivation, UserRegistration, UserNewActivationLink, UserWelcomePage, UserAccountConformation


urlpatterns = [


    url(r'^$', UserWelcomePage.as_view(), name='welcome_page'),
    url(r'^conformation/$', UserAccountConformation.as_view(), name='welcome_page'),
	url(r'^register/$', UserRegistration.as_view(), name='new_user_registration'),
	url(r'^activate/(?P<key>.+)$', UserActivation.as_view(), name='activate_new_user'),
	url(r'^new-activation-link/(?P<user_id>\d+)/$', UserNewActivationLink.as_view(), name='send_new_activation_link'),


]
