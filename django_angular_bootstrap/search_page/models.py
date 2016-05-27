from django.db import models


class Recipe(models.Model):
    class Meta:
        verbose_name = 'Рецепт'

    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    class Meta:
        verbose_name = 'Список ингредиентов'

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AlterIngredient(models.Model):
    class Meta:
        verbose_name = 'Заменяемые ингредиенты'

    ingredient = models.ForeignKey(Ingredient, related_name='id_ingredient')
    alternative = models.ManyToManyField(Ingredient, related_name='id_complimentary_ingredient')

    def __str__(self):
        return self.ingredient.name + '+alt'

class ListIngredient(models.Model):
    class Meta:
        verbose_name = 'Список ингредиентов в рецепте'

    recipe = models.ForeignKey(Recipe, related_name='id_recipe')
    alteringredient = models.ManyToManyField(AlterIngredient, related_name='id_ingridient_w_alter', blank=True)
    ingredient = models.ManyToManyField(Ingredient, related_name='id_ingridient_wo_alter')

    def __str__(self):
        return self.recipe.name

