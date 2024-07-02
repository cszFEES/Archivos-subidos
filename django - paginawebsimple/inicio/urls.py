from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mecenas', views.mecenas, name='mecenas'),
    path('mecenazgo', views.mecenazgo, name='mecenazgo'),
]
