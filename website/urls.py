from django.urls import path
from . import views
from .views import ProgramDetailView
from .views import FollowedProgramView
from .views import FollowedProgramConfirmationView
from django.contrib.auth.views import LogoutView
from .views import create_program
from .views import ArticleDetailView
from .views import load_states, load_cities
from .views import unfollow_program
from .views import all_photos_view



class LogoutAndStay(LogoutView):
    next_page = '/'
    def get_next_page(self):
        return self.request.META.get('HTTP_REFERER', super().get_next_page())
    
    
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.ProgramSearchView, name='program_search'),
    path('program/<slug:slug>/', ProgramDetailView.as_view(), name='program_detail'),
    path('program_register/<int:program_id>/', FollowedProgramView.as_view(), name='program_register'),
    path('followedprogram/confirmation/', FollowedProgramConfirmationView.as_view(), name='followed-program-confirmation'),
    path('logout/', LogoutAndStay.as_view(), name='logout'),
    path('create_program/', create_program, name='create_program'),
    path('programmes-suivis/', views.ProgrammesSuivisView.as_view(), name='programmes_suivis'),
    path('article/category/<slug:category_slug>/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/category/<slug:category_slug>/', views.category_articles, name='category_articles'),
    path('categories/<slug:category_slug>/', views.category_articles, name='category_articles'),
    path('ajax/load-states/', load_states, name='ajax_load_states'),
    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
    path('unfollow_program/<int:program_id>/', unfollow_program, name='unfollow_program'),
    path('photos/', all_photos_view, name='all_photos'),
]
