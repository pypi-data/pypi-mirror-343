from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from microaAdmin.models import *
from parler.admin import TranslatableAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Əlavə məlumatlar", {"fields": ("phone_number", "birth_date")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Əlavə məlumatlar", {"fields": ("phone_number", "birth_date")}),
    )

#
class CategoryImageInline(admin.TabularInline):
    model = PageImage
    extra = 1

@admin.register(Page)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'title', 'description', 'icon', 'slug', 'order', 'is_active', 'user', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)
    
    inlines = [CategoryImageInline]
    readonly_fields = ['slug']

##
class SubcategoryImageInline(admin.TabularInline):
    model = SubcategoryImage
    extra = 1

@admin.register(Subpage)
class SubcategoryAdmin(TranslatableAdmin):
    list_display = ('id', 'category', 'parent', 'name', 'title', 'description', 'icon', 'slug', 'full_slug', 'order', 'is_active', 'user', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

    inlines = [SubcategoryImageInline]
    readonly_fields = ['slug', 'full_slug']