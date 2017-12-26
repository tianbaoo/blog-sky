"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^layout_category/(?P<user_id>\d+).html', views.layout_category),
    url(r'^edit_category/', views.edit_category),
    url(r'^add_category.html/', views.add_category),

    url(r'^layout_tag/(?P<user_id>\d+).html', views.layout_tag),
    url(r'^edit_tag/', views.edit_tag),
    url(r'^add_tag.html/', views.add_tag),

    url(r'^index/', views.index),
    url(r'^all/(?P<type_id>\d+)/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^check_code/', views.check_code),
    url(r'^updown', views.updown),
    url(r'^logout/', views.logout),
    url(r'^comments-(?P<nid>\d+).html', views.comments),
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html$', views.article),
    url(r'^(?P<site>\w+)/(?P<key>((tag)|(create_time)|(category)))/(?P<val>\w+-*\w*)/', views.filter),
    url(r'^(\w+)/$', views.home),
    url(r'^management/(?P<user_id>\d+)-(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<tags__nid>\d+)', views.management),
    url(r'^add_article/(?P<blog_id>\d+)', views.add_article),
    url(r'^upload_img.html', views.upload_img),

    url(r'^', views.index),

]
