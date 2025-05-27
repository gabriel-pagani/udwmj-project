from django.contrib import admin
from app.models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = 'title',
    list_editable = 'is_published',
    search_fields = 'title', 'description',
    list_filter = 'category', 'is_published',
    ordering = '-id',
\


admin.site.register(Category, CategoryAdmin)
