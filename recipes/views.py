from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

# from .utils.recipes.factory import make_recipe
from recipes.models import Recipes

# Esse está buscando dentro da namespace, recipes, em templates.
# No render também, você pode passar os Status HTTP, exemplo de como passar 201
# Também é possível enviar variáveis no render, exemplo.


def home(request):
    """ print(make_recipe() """
    # ex = User._meta.get_fields()
    # print(ex)
    # Colocando um Filtro para mostrar somente receitas que estão publicadas.
    '''recipes = Recipes.objects.filter(
        is_published=True,
    ).order_by('-id')'''
    # Simplificando a Consulta acima.
    recipes = Recipes.objects.filter(
        is_published=True
    ).order_by('-id')
    """ valor = Recipes._meta.get_fields()[14]
    print(valor)
    b = recipes.first().category
    a = recipes.last().category.id
    print(a, b) """
    return render(request, 'recipes/pages/home.html', status=200, context={
        'name': 'Receitas Brasileiras',
        # 'recipes': [make_recipe() for _ in range(3)],
        'recipes': recipes,
    })


def category(request, category_id):
    """ recipes = Recipes.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by('-id')
    print(category_id) """

    # Exemplo de Como pegar o Atributo de um Objeto/Classe, Mantido como Ex.
    """ category_name = getattr(
        getattr(recipes.first(), 'category', None),
        'name',
        'Not Found'
    ) """

    """ if not recipes:
        raise Http404('Não encontrado!') """
    # Usando esse função é possível passar o model, mas a melhor maneira
    # é no exemplo abaixo.
    """ recipes = get_list_or_404(Recipes, category__id=category_id,
                              is_published=True,) """
    recipes = get_list_or_404(
        Recipes.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )

    return render(request, 'recipes/pages/category.html', context={
        'name': 'Receitas Brasileiras',
        'title': f'{recipes[0].category.name} | Recipes',
        'recipes': recipes,
    })


def recipe(request, id):
    '''recipe = Recipes.objects.filter(
        pk=id,
        ).order_by('-id').first()'''
    # Simplificando o código acima, com a Função get_object_or_404
    recipe = get_object_or_404(Recipes, pk=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'name': 'Receitas Brasileiras',
        'recipe': recipe,
        'is_detail_page': True,
        'detail_on': True,
    })


# Esse vai buscar dentro da namespace, Global, dentro da base_templates.
def home_global(request):
    return render(request, 'global/home.html')


def sobre(request):
    return HttpResponse('sobre')


def contato(request):
    # Como eu coloquei o caminho completo no base dir, ele acha o arquivo
    # procurando só no caminho informado, exemplo comentado.
    # return render(request, 'temp.html', status=200)
    # para ficar mais claro, vamos criar um namespace e colocar o endereço com
    # namespace para evitar confusão.
    return render(request, 'pesquise_aqui/temp.html', status=200)


def search(request):
    return render(request, 'recipes/pages/search.html')
    # atualizando
