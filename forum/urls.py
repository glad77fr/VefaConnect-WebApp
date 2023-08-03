from django.urls import path
from . import views
from .views import contact_view

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('contact/', contact_view, name='contact'),
    path('profile/', views.profile, name='profile'),
    

]
