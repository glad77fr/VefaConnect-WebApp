from django.urls import path
from . import views
from .views import ProgramDetailView
from .views import FollowedProgramView
from .views import FollowedProgramConfirmationView
from django.contrib.auth.views import LogoutView


class LogoutAndStay(LogoutView):
    def get_next_page(self):
        return self.request.META.get('HTTP_REFERER', super().get_next_page())
    
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.ProgramSearchView, name='program_search'),
    path('program/<slug:slug>/', ProgramDetailView.as_view(), name='program_detail'),
    path('program_register/<int:program_id>/', FollowedProgramView.as_view(), name='program_register'),
    path('followedprogram/confirmation/', FollowedProgramConfirmationView.as_view(), name='followed-program-confirmation'),
    path('logout/', LogoutAndStay.as_view(), name='logout')
]
