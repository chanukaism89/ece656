from collections import Counter

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from recipes.models import recipes, ingredients

class HelloView(TemplateView):
    def get(self,request, **kwargs):
        context = {
            "most_visited": recipes.objects.get_most_visited(),
            "most_favourited": recipes.objects.get_most_favourited(),
            "recently_added": recipes.objects.get_recently_added(),
            }


        return render(request, 'recipes/hello.html', context=context)

# Create your views here.
class LandingPageView(TemplateView):
    def get(self, request, **kwargs):
        context = {
            "most_visited": recipes.objects.get_most_visited(),
            "most_favourited": recipes.objects.get_most_favourited(),
            "recently_added": recipes.objects.get_recently_added(),
        }
        return render(request, "recipes/home.html", context=context)


# Create your views here.
class MostVisitedPageView(TemplateView):
    def get(self, request, **kwargs):
        context = {
            "most_visited": recipes.objects.get_most_visited(limit=50),
        }
        return render(request, "recipes/most_visited.html", context=context)


# Create your views here.
class MostFavouritedPageView(TemplateView):
    def get(self, request, **kwargs):
        context = {
            "most_favourited": recipes.objects.get_most_favourited(limit=50),
        }
        return render(request, "recipes/most_favourited.html", context=context)


class RecentlyAddedPageView(TemplateView):
    def get(self, request, **kwargs):
        context = {
            "recently_added": recipes.objects.get_recently_added(limit=50),
        }
        return render(request, "recipes/recently_added.html", context=context)


# Create your views here.
class RecipeDetailsPageView(TemplateView):
    def get(self, request, **kwargs):
        recipe = get_object_or_404(recipes, recipe_id=kwargs["recipe_id"])
        preparation_steps = recipe.get_preparation_steps_in_order()
        similar_recipes = recipe.find_similar_recipes(limit=3)

        # has the logged in user liked these recipes?
        liked = False
        # if request.user.username and request.user in recipe.liked_by_users.all():
         #   liked = True

        recipe.recipe_visits += 1
        recipe.save()

        context = {
            "recipe": recipe,
            "preparation_steps": preparation_steps,
            "similar_recipes": similar_recipes,
            "liked": liked,
        }
        return render(request, "recipes/recipe_details.html", context=context)


class RecipeLikeApiView(View):
    def post(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs["recipe_id"])
        recipe.liked_by_users.add(request.user)
        recipe.likes = recipe.likes + 1
        recipe.save()
        return JsonResponse(
            {"recipe_id": recipe.id, "user_id": request.user.id, "success": True,}
        )


class RecipeUnlikeApiView(View):
    def post(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs["recipe_id"])
        recipe.liked_by_users.remove(request.user)
        recipe.likes = recipe.likes - 1
        recipe.save()
        return JsonResponse(
            {"recipe_id": recipe.id, "user_id": request.user.id, "success": True,}
        )


class RecipeSearchResultsView(TemplateView):
    def get(self, request, **kwargs):
        query = request.GET["q"] or ""
        search_terms = query.split(" ")

        recipe_counter = Counter()

        # search for recipes containing the search terms in their names
        for term in search_terms:
            recipe_counter.update(Recipe.objects.filter(name__icontains=term).all())

        all_ingredients = set()
        for term in search_terms:
            for ingredient in ingredients.objects.filter(name__icontains=term).all():
                all_ingredients.add(ingredient)

        for ingredient in all_ingredients:
            recipe_counter.update(ingredient.recipes.all())

        search_results = [recipe for (recipe, _) in recipe_counter.most_common(50)]

        context = {
            "search_results": search_results[:50],
            "query": query,
        }

        return render(request, "recipes/search_results.html", context=context)
