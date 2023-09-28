from django.urls import path
from . import views
from .views import contact_view
from .views import general_forum_view
from .views import ForumThemeView
from .views import CreatePostView
from .views import PostDetailView
from .views import reply_to_post
from .views import access_denied


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('contact/', contact_view, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('general_forum/<slug:topic_slug>/create_post/', CreatePostView.as_view(), name='create_post_general'),
    path('program_forum/<slug:program_slug>/<slug:topic_slug>/create_post/',CreatePostView.as_view(), name='create_post_with_program'),
    path('general_forum/', general_forum_view, name='general_forum'),
    path('topic/<slug:topic_slug>/', ForumThemeView.as_view(), name='general_forum_theme_detail'),
    path('program_forum/<slug:program_slug>/topic/<slug:topic_slug>/', ForumThemeView.as_view(), name='forum_theme_detail'),
    path('general_forum/<slug:topic_slug>/<slug:post_slug>/', views.PostDetailView.as_view(), name='general_post_detail'),
    path('program_forum/<slug:program_slug>/<slug:topic_slug>/<slug:post_slug>', views.PostDetailView.as_view(), name='program_post_detail'),
    path('post/<int:post_id>/reply/', reply_to_post, name='reply_to_post'),
    path('access-denied/', access_denied, name='access_denied'),
    path('program_forum/<slug:program_slug>/', views.ProgramForumView.as_view(), name='program_forum'),
]
