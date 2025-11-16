from django.db import models
from django.conf import settings


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.JSONField()
    steps = models.JSONField()
    time = models.CharField(max_length=64, blank=True)
    difficulty = models.CharField(max_length=16, choices=[('easy','Easy'),('medium','Medium'),('hard','Hard')], default='easy')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_history')
    ingredients_raw = models.TextField()
    response_time = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SavedRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.recipe}"
