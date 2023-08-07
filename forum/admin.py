from django.contrib import admin

from .models import UserProfile, Forum, ForumTheme, ForumPost, Reply

# Configuration de l'administration pour le modèle UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined_date',"first_name","last_name","gender")
    list_filter = ('joined_date',)
    search_fields = ('user__username', 'user__email')

# Configuration de l'administration pour le modèle Forum
@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Configuration de l'administration pour le modèle ForumTheme
@admin.register(ForumTheme)
class ForumThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'forum','order','slug')
    list_filter = ('forum','order')

# Configuration de l'administration pour le modèle ForumPost
@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'real_estate_program', 'date_posted')
    list_filter = ('theme__forum', 'real_estate_program')
    search_fields = ('user__username', 'theme__title', 'content')

# Configuration de l'administration pour le modèle Reply
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'date_posted')
    list_filter = ('post__theme__forum',)
    search_fields = ('user__username', 'post__theme__title', 'content')

