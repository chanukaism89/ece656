from collections import Counter

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from recipes.models import recipes, ingredients, likes

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
        ingredient_names = recipe.get_ingredients()
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
            "ingredients": ingredient_names,
        }
        return render(request, "recipes/recipe_details.html", context=context)


class RecipeLikeApiView(View):
    def post(self, request, **kwargs):
        recipe = get_object_or_404(recipes, recipe_id=kwargs["recipe_id"])
        liked_entry = likes.objects.filter( recipe_id=kwargs["recipe_id"], user_id=request.user.id)
        print (liked_entry)
        if(liked_entry):
            print("liked entry found")
            liked_entry[0].is_like = 1
            liked_entry[0].save()
        else:
            print("No liked entry found")
            like = likes(is_like=1, recipe_id=recipe, user_id=request.user)
            like.save()
        recipe.recipe_likes += 1
        recipe.save()
        return JsonResponse(
            {"recipe_id": recipe.recipe_id, "user_id": request.user.id, "success": True,}
        )


class RecipeUnlikeApiView(View):
    def post(self, request, **kwargs):
        recipe = get_object_or_404(recipes, recipe_id=kwargs["recipe_id"])
        like = likes(is_like=0, recipe_id=recipe, user_id=request.user)
        liked_entry = likes.objects.filter( recipe_id=kwargs["recipe_id"], user_id=request.user.id)
        liked_entry[0].is_like = 0
        liked_entry[0].save()
        recipe.recipe_likes -= 1
        recipe.save()
        return JsonResponse(
            {"recipe_id": recipe.recipe_id, "user_id": request.user.id, "success": True,}
        )


class RecipeSearchResultsView(TemplateView):
    def get(self, request, **kwargs):
        query = request.GET["q"] or ""
        search_terms = query.split(" ")

        recipe_counter = Counter()

        # search for recipes containing the search terms in their names
        for term in search_terms:
            
            recipe_counter.update(recipes.objects.filter(recipe_name__iregex=r"\b{0}\b".format(term)).all())

        all_ingredients = set()
        for term in search_terms:
            for ingredient in ingredients.objects.filter(ingredient_name__iregex=r"\b{0}\b".format(term)).all():
                all_ingredients.add(ingredient)
                #print (all_ingredients)
        #print (all_ingredients)
        for ingredient in all_ingredients:
            recipe_list =[]
            recipe_map_list= ingredient.get_recipes()
            #print (recipe_list)

            if recipe_map_list:
                
                for mapping in recipe_map_list:

                    #print (ingredient)
                    #print (recipe_list)
                    recipe_counter.update(recipes.objects.filter(recipe_name=mapping))
                     
        search_results = [recipe for (recipe, _) in recipe_counter.most_common(50)]

        context = {
            "search_results": search_results[:50],
            "query": query,
        }

        return render(request, "recipes/search_results.html", context=context)
