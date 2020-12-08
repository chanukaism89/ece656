from django.contrib import admin
from .models import recipes, ingredients

# Register your models here.

admin.site.register(recipes)
admin.site.register(ingredients)


