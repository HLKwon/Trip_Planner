from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^add/newtrip$', views.newtrip),
    url(r'^logout$', views.logout),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),
    url(r'^join/(?P<id>\d+)$', views.join, name='join'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^edited/(?P<id>\d+)$', views.edited, name='edited'),
]
