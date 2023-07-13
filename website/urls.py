from django.urls import path
from . import views
from .views import ProgramDetailView


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.ProgramSearchView, name='program_search'),
    path('program/<slug:slug>/', ProgramDetailView.as_view(), name='program_detail'),
]
