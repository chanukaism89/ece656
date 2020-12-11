from django.db import models
from datetime import date
import arrow
from collections import Counter
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class recipesManager(models.Manager):

    def get_most_visited(self, limit=3):
        assert limit > 0
        return self.order_by("-recipe_visits").all()[:limit]

    def get_most_favourited(self, limit=3):
        assert limit > 0
        return self.order_by("-recipe_likes").all()[:limit]

    def get_recently_added(self, limit=3):
        assert limit > 0
        return self.order_by("-recipe_submitted_date").all()[:limit]




class recipes(models.Model):
    recipe_id = models.IntegerField(primary_key=True)
    recipe_name = models.TextField()
    recipe_websearch_id = models.IntegerField()
    recipe_cooktime = models.IntegerField()
    recipe_submitted_date = models.DateField(default=date.today())
    recipe_numof_steps = models.IntegerField()
    recipe_numof_ingredients = models.IntegerField()
    recipe_description = models.TextField()
    recipe_contributor = models.TextField(default='Food.com')
    recipe_likes = models.IntegerField(default=0)
    recipe_visits = models.IntegerField(default=0)
    objects = recipesManager()

    def __str__(self):
        return self.recipe_name

    def human_readable_submitted_date(self):
        return arrow.get(self.recipe_submitted_date).humanize()

    def get_preparation_steps_in_order(self):
        return self.preparation_steps.order_by("step_number").all()

    def find_similar_recipes(self, limit=3):
        recipe_counter = Counter()
        #print (self.ingredients.all())
        #print (self.preparation_steps.all())
        for ingredient in self.ingredients.all():
            #print (self.ingredients.all())
            top_recipes = (
                recipes.objects.exclude(recipe_id=self.recipe_id)
                .filter(ingredients__ingredient_id=ingredient.ingredient_id)
                .order_by("-recipe_likes")
                .all()[:limit]
            )
            recipe_counter.update(top_recipes)

        similar_recipes = [r for (r, _) in recipe_counter.most_common(limit)]
        #print (similar_recipes)
        return similar_recipes

    def get_ingredients(self):
        name_list =[]
        for ingredient in self.ingredients.all():
            name_list.append(ingredient.ingredient_id)
            
        print (name_list)
        return name_list

    class Meta:
        verbose_name="All Recipes"
        verbose_name_plural="Recipies List"

class ingredients(models.Model):
    ingredient_id = models.IntegerField(primary_key=True)
    ingredient_name = models.TextField()
    ingredient_vists = models.IntegerField(default=0)

    def get_recipes(self):
        map_list =[]
        recipe_id_list =[]
        #print (self)
        #print (self.ing_id.all())
        map_list = self.ing_id.all()
        
        
        for mapping in map_list:
            recipe_id_list.append (mapping.recipe_id)
        #print (recipe_id_list)
        return recipe_id_list

    def __str__(self):
        return self.ingredient_name

    class Meta:
    
        verbose_name="All Ingredients"
        verbose_name_plural="Ingredients List"

class recipe_ingredient_mapping_names(models.Model):

    mapping_id = models.IntegerField(primary_key=True)
    recipe_id = models.ForeignKey(recipes, on_delete=models.CASCADE, related_name="ingredients1")
    ingredient_name = models.ForeignKey(ingredients, on_delete=models.CASCADE, related_name="ing_name")


class recipe_prep_steps(models.Model):
                        
    steps_id = models.IntegerField(primary_key=True)
    recipe_id = models.ForeignKey(recipes,on_delete=models.CASCADE, related_name="preparation_steps")
    step_description = models.TextField()
    step_number = models.IntegerField()

class recipe_ingredient_mapping(models.Model):
        
    mapping_id = models.IntegerField(primary_key=True)
    recipe_id = models.ForeignKey(recipes, on_delete=models.CASCADE , related_name="ingredients")
    ingredient_id = models.ForeignKey(ingredients, on_delete=models.CASCADE, related_name="ing_id")
