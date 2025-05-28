from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from app.models import Recipe


def home(request):
    search_query = request.GET.get('search', '').strip()
    published_recipes = Recipe.objects.filter(
        is_published=True).select_related('category', 'author')

    if search_query:
        published_recipes = published_recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

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

    context = {
        'recipes': recipes,
        'search_query': search_query,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'app/partials/recipe_grid.html', context)

    return render(request, 'app/home.html', context)


def about(request):
    return render(request, 'app/about.html')


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=True)
    return render(request, 'app/recipe.html', {'recipe': recipe})
