from django.contrib import admin
from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [

    path('search_recipes/', views.search_using_recipes, name='search_using_recipe'),
    # path('search_using_ing/', views.search_using_ingredients, name='search_using_ingredients'),

]
