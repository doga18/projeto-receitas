from django.urls import path

from . import views

# recipes:recipes
app_name = 'recipes'

# O Raiz desse APP, é o domínio.com/recipes/
# O Sobre seria, domínio.com/recipes/sobre
urlpatterns = [
    path('', views.home, name="home"),
    # Quanto mais específico, deixe mais acima.
    # Muito específico.
    path('recipes/search/', views.search, name="search"),
    # Menos específico.
    path('recipes/category/<int:category_id>/',
         views.category,
         name="category"
         ),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
    path('home_global', views.home_global),
    path('sobre/', views.sobre),
    path('contato/', views.contato),
]
