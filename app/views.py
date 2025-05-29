from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from app.models import Recipe, Favorite, Category
from django.contrib.postgres.search import TrigramSimilarity


def home(request):
    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', '').strip()
    selected_prep_time = request.GET.get('prep_time', '').strip()
    selected_servings = request.GET.get('servings', '').strip()
    favorites_only = request.GET.get('favorites', '').strip() == 'true'

    published_recipes = Recipe.objects.filter(
        is_published=True).select_related('category', 'author')

    if search_query:
        try:
            published_recipes = published_recipes.annotate(
                similarity_title=TrigramSimilarity('title', search_query),
                similarity_desc=TrigramSimilarity('description', search_query),
                similarity_cat=TrigramSimilarity('category__name', search_query),
            ).filter(
                Q(similarity_title__gt=0.2) |
                Q(similarity_desc__gt=0.2) |
                Q(similarity_cat__gt=0.2) |
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            ).order_by(
                '-similarity_title', '-similarity_desc', '-similarity_cat'
            )

        except Exception:
            published_recipes = published_recipes.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

    if selected_category:
        published_recipes = published_recipes.filter(
            category__name=selected_category)

    if selected_prep_time:
        if selected_prep_time == '0-30':
            published_recipes = published_recipes.filter(
                preparation_time__lte=30)
        elif selected_prep_time == '31-60':
            published_recipes = published_recipes.filter(
                preparation_time__gte=31, preparation_time__lte=60)
        elif selected_prep_time == '60+':
            published_recipes = published_recipes.filter(
                preparation_time__gt=60)

    if selected_servings:
        if selected_servings == '1-2':
            published_recipes = published_recipes.filter(
                servings__gte=1, servings__lte=2)
        elif selected_servings == '3-4':
            published_recipes = published_recipes.filter(
                servings__gte=3, servings__lte=4)
        elif selected_servings == '5+':
            published_recipes = published_recipes.filter(servings__gte=5)

    user_favorites = set()
    if request.user.is_authenticated:
        user_favorites = set(
            Favorite.objects.filter(user=request.user).values_list(
                'recipe_id', flat=True)
        )
        if favorites_only:
            published_recipes = published_recipes.filter(id__in=user_favorites)
    else:
        if favorites_only:
            published_recipes = Recipe.objects.none()

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

    categories = Category.objects.all()

    context = {
        'recipes': recipes,
        'search_query': search_query,
        'categories': categories,
        'selected_category': selected_category,
        'selected_prep_time': selected_prep_time,
        'selected_servings': selected_servings,
        'favorites_only': favorites_only,
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
