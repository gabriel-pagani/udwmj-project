from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from app.forms import LoginForm, CustomPasswordChangeForm, RegisterForm, RecipeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from app.models import Recipe, Favorite, Category
from rapidfuzz import fuzz


def home(request):
    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', '').strip()
    selected_prep_time = request.GET.get('prep_time', '').strip()
    selected_servings = request.GET.get('servings', '').strip()
    favorites_only = request.GET.get('favorites', '').strip() == 'true'

    published_recipes = Recipe.objects.filter(
        is_published=True).select_related('category', 'author')

    if search_query:
        filtered_recipes = []
        search_lower = search_query.lower()

        for recipe in published_recipes:
            title_score = fuzz.partial_ratio(
                search_lower, recipe.title.lower())
            desc_score = fuzz.partial_ratio(
                search_lower, recipe.description.lower())
            cat_score = fuzz.partial_ratio(
                search_lower, recipe.category.name.lower() if recipe.category else '')

            max_score = max(title_score, desc_score, cat_score)
            if max_score > 75:
                filtered_recipes.append((recipe, max_score))

        filtered_recipes.sort(key=lambda x: x[1], reverse=True)
        published_recipes = [recipe for recipe, score in filtered_recipes]

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


def login_view(request):
    form = LoginForm()
    return render(request, 'app/auth/login.html', {
        'form': form,
        'form_action': reverse('app:login_done')
    })


def login_done(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data.get('username', '')
        password = form.cleaned_data.get('password', '')

        user = authenticate(
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect(reverse('app:home'))
        else:
            messages.error(request, 'Invalid data')
    else:
        messages.error(request, 'Fill in all fields')

    return redirect(reverse('app:login'))


@login_required
def change_password_view(request):
    user = request.user
    form = CustomPasswordChangeForm(user, request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            saved_user = form.save()
            update_session_auth_hash(request, saved_user)
            return redirect(reverse('app:home'))

        else:
            old_password = form.data.get('old_password', '')
            new_password1 = form.data.get('new_password1', '')
            new_password2 = form.data.get('new_password2', '')

            if not old_password or not new_password1 or not new_password2:
                erro_mensagem = "Fill in all fields"
            elif 'old_password' in form.errors:
                erro_mensagem = "Current password is incorrect"
            elif new_password1 != new_password2:
                erro_mensagem = "Passwords do not match"
            elif len(new_password1) < 8 and new_password1.isdigit():
                erro_mensagem = "The new password must be at least 8 characters long and cannot be entirely numeric."
            elif 'new_password1' in form.errors:
                erro_mensagem = "The new password does not meet security requirements"
            else:
                erro_mensagem = "An error occurred while changing your password. Please check your details and try again."

            messages.error(request, erro_mensagem)

    return render(request, 'app/auth/change_password.html', {
        'form': form,
    })


@login_required
def logout_view(request):
    logout(request)
    return redirect('app:home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('app:home')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            # Authenticate and login automatically after registration
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if user:
                login(request, user)
                return redirect('app:home')
        else:
            # Custom error handling
            if form.errors:
                error_messages = []

                # Check specific errors
                if 'username' in form.errors:
                    if 'already in use' in str(form.errors['username']):
                        error_messages.append(
                            'This username is already in use.')
                    else:
                        error_messages.append('Invalid username.')

                if 'password1' in form.errors:
                    error_messages.append(
                        'Password does not meet security requirements.')

                if 'password2' in form.errors:
                    error_messages.append('Passwords do not match.')

                # If no specific errors, use generic message
                if not error_messages:
                    error_messages.append(
                        'Please check the information provided and try again.')

                for error_msg in error_messages:
                    messages.error(request, error_msg)

    return render(request, 'app/auth/register.html', {
        'form': form,
    })


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(
                request, 'Your recipe has been sent for analysis.')
            return redirect('app:home')
        else:
            # Handle form errors
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(
                            request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = RecipeForm()

    return render(request, 'app/recipe_form.html', {
        'form': form,
    })
