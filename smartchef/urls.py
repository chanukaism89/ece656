"""smartchef URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
import recipes.views
import account.views
from django.contrib.auth import views as auth_views

urlpatterns = [
            
    path("", recipes.views.LandingPageView.as_view(), name="landing_page"),
    path("account/", include("django.contrib.auth.urls")),
    path("account/login", account.views.LoginView.as_view(), name='login'),
    path("account/register/", account.views.CreateUserView.as_view(), name="register_user",),
    path("trending/",recipes.views.MostVisitedPageView.as_view(), name="trending_recipes_page",),
    path("recent/",recipes.views.RecentlyAddedPageView.as_view(),name="recently_added_recipes_page",),
    path("favourites/",recipes.views.MostFavouritedPageView.as_view(), name="most_favourited_recipes_page",),
    path("recipe/<int:recipe_id>/", recipes.views.RecipeDetailsPageView.as_view(),name="recipe_detail_page",),
    path("recipe/<int:recipe_id>/like",recipes.views.RecipeLikeApiView.as_view(), name="recipe_like_view",),
    path("recipe/<int:recipe_id>/unlike",recipes.views.RecipeUnlikeApiView.as_view(), name="recipe_unlike_view",),
    path("recipe/search",recipes.views.RecipeSearchResultsView.as_view(), name="recipe_search_results_view",),
    path("admin/", admin.site.urls),
    path("hello/", recipes.views.HelloView.as_view(), name="hello"),

                                                   

]
