from django.shortcuts import render, get_object_or_404
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

    return render(request, 'app/home.html', {'recipes': recipes})


def about(request):
    return render(request, 'app/about.html')


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=True)
    return render(request, 'app/recipe.html', {'recipe': recipe})
