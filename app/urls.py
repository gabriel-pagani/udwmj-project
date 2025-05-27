from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]
