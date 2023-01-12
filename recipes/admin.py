from django.contrib import admin
from .models import Category, Recipes


# Para pegar todos os campos de uma Class você pode usar o _meta
# Exemplo: Classe._meta.get_fields()
# Prático: User._meta.get_fields()
# Pegando por índices, User._meta.get_fields()[0]
# EX: Pegando o Value do índice, getattr(User, 'field')
# Prático: getattr(User, 'id')
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    ...


""" class RecipesAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'description',
                    'slug',
                    'preparation_time',
                    'preparation_time_unit',
                    'servings',
                    'servings_unit',
                    'preparation_steps',
                    'preparation_steps_unit',
                    'preparation_steps_is_html',
                    'created_at',
                    'updated_at',
                    'is_published',
                    'cover',
                    'category',
                    'author'
                    ) """


admin.site.register(Category, CategoryAdmin)
""" admin.site.register(Recipes, RecipesAdmin) """
