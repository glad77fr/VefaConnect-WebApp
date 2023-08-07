from django.urls import path
from . import views
from .views import contact_view
from .views import general_forum_view
from .views import ForumThemeView
from .views import CreatePostView
from .views import PostDetailView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('contact/', contact_view, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('general_forum/', general_forum_view, name='general_forum'),
    path('topic/<slug:topic_slug>/', ForumThemeView.as_view(), name='forum_theme_detail'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail')   
    
]
