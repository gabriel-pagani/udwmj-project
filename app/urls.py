from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('login/', views.login_view, name='login'),
    path('login/done', views.login_done, name='login_done'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
]
