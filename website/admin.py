from django.contrib import admin
from .models import RealEstateDeveloper, RealEstateProgram, FollowedProgram, Country, City, Address

@admin.register(RealEstateDeveloper)
class RealEstateDeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(RealEstateProgram)
class RealEstateProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'developer')
    list_filter = ('developer',)
    search_fields = ('name', 'location', 'developer__name')

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
    list_filter = ('country',)
    search_fields = ('name', 'country__name')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'country')
    list_filter = ('country', 'city__country')
    search_fields = ('street', 'city__name', 'country__name')