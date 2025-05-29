from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from app.models import Recipe, Favorite


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

    user_favorites = set()
    if request.user.is_authenticated:
        user_favorites = set(
            Favorite.objects.filter(user=request.user).values_list(
                'recipe_id', flat=True)
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
            recipe.id in user_favorites,
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


@login_required
@require_POST
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, is_published=True)

    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        recipe=recipe
    )

    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True

    return JsonResponse({
        'is_favorited': is_favorited,
        'message': 'Recipe added to favorites' if is_favorited else 'Recipe removed from favorites'
    })
