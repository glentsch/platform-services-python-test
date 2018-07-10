from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Orders_View.as_view(), name='orders'),
]
