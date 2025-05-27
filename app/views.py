from django.shortcuts import render
from app.models import Recipe


def home(request):
    published_recipes = Recipe.objects.filter(
        is_published=True).select_related('category', 'author')

    recipes = dict()
    for recipe in published_recipes:
        recipes[f'{recipe.id}'] = [
            recipe.title,
            recipe.description,
            recipe.instructions,
            recipe.preparation_time,
            recipe.servings,
            recipe.cover,
            recipe.category.name if recipe.category else None,
            recipe.author.username if recipe.author else None,
            recipe.updated_at,
            recipe.created_at,
            recipe.is_published,
        ]

    return render(request, 'app/index.html', {'recipes': recipes})
