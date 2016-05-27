from django.contrib import admin
from .models import Recipe, Ingredient, AlterIngredient, ListIngredient


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(AlterIngredient)
admin.site.register(ListIngredient)