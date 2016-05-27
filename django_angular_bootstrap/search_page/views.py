import json
from django.http import HttpResponse
from django.shortcuts import render

from .models import Ingredient, Recipe, AlterIngredient, ListIngredient


def index(request):
    return HttpResponse("Hello, world!")

def search_result(request, search):
    result_dict = {}
    meals_list = []
    result_dict['count'] = len(Recipe.objects.all())
    list_recipes_w_ing = ListIngredient.objects.all()
    for recipe in list_recipes_w_ing:
        meal = {}
        meal['name'] = recipe.recipe.name
        meal['ingredients'] = [i.name for i in recipe.ingredient.all()]
        for alt_ingr in  recipe.alteringredient.all():
            alternative_list = [a.name for a in alt_ingr.alternative.all()]
            alt_ingredients = '{} или {}'.format(alt_ingr.ingredient.name, ' или '.join(alternative_list))
            meal['ingredients'].append(alt_ingredients)
        meals_list.append(meal)
    result_dict['meals'] = meals_list
    return HttpResponse(json.dumps(result_dict, ensure_ascii=False),
                        content_type='application/json; encoding=utf-8')
