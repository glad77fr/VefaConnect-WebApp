from django.contrib import admin
from .models import RealEstateDeveloper, RealEstateProgram,UnvalidatedRealEstateProgram, ProgramPhoto,PhotoCategory
from .models import FollowedProgram, Country, City, Address, State
from .models import Article, Section, Category

@admin.register(RealEstateDeveloper)
class RealEstateDeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','slug')
    search_fields = ('name', 'description','slug')

@admin.register(RealEstateProgram)
class RealEstateProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'developer','date_added', 'end_date', 'validated','slug']
    list_filter = ['validated','developer','date_added','slug']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(validated=True)

@admin.register(UnvalidatedRealEstateProgram)
class UnvalidatedRealEstateProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'developer', 'end_date']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(validated=False)

@admin.register(FollowedProgram)
class FollowedProgramAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'real_estate_program', 'date_followed', 'is_owner')
    list_filter = ('user_profile', 'real_estate_program', 'is_owner')
    search_fields = ('user_profile__user__username', 'real_estate_program__name', 'apartment_lot_reference')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('name', 'country')
    search_fields = ('name', 'country__name')

    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'country')
    list_filter = ('country', 'city__country')
    search_fields = ('street', 'city__name', 'country__name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'city':
            kwargs["queryset"] = City.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'author',)
    search_fields = ('title', 'author__username',)
    list_filter = ('publication_date', 'author',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('associated_articles',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('type', 'article',)
    list_filter = ('type',)
    search_fields = ('article__title',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description',)
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(State)
class RealEstateDeveloperAdmin(admin.ModelAdmin):
    list_display = ('code', 'name','country')
    search_fields = ('code', 'name','country')

@admin.register(ProgramPhoto)
class ProgramPhotoAdmin(admin.ModelAdmin):
    list_display = ('real_estate_program', 'caption', 'uploaded_by', 'upload_date', 'category')
    list_filter = ('real_estate_program', 'upload_date', 'category')
    search_fields = ('caption', 'real_estate_program__name', 'uploaded_by__username')
    raw_id_fields = ('uploaded_by',)  # Permet de rechercher et sélectionner les utilisateurs plus facilement
    date_hierarchy = 'upload_date'  # Navigation rapide à travers les dates
    ordering = ('-upload_date',)

@admin.register(PhotoCategory)
class PhotoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)