# Para importar variáveis de ambiente, é necessário importar o OS. Continua na linha 21 # noqa: 501
import os

# O Q serve para informar ao django que você quer o and ou or na busca.
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, render

# from .utils.recipes.factory import make_recipe
from recipes.models import Recipes

from .tests.generator_pagination import make_pagination

# Esse está buscando dentro da namespace, recipes, em templates.
# No render também, você pode passar os Status HTTP, exemplo de como passar 201
# Também é possível enviar variáveis no render, exemplo.

# Nome do Site.
name_of_site = os.environ.get('NAME_OF_SITE')

# POR PÁGINAS

# Continuando a parte de importações, depois importar a variável, se não tiver nada na variável, use o valor 6 # noqa: 501
PER_PAGES = os.environ.get('PER_PAGE', 6)


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

    # Oque ele faz, ele tenta pegar a chave page e o seu valor, caso não tenha, usa o valor 1 # noqa: 501

    """ valor = Recipes._meta.get_fields()[14]
    print(valor)
    b = recipes.first().category
    a = recipes.last().category.id
    print(a, b) """

    # messages.info(request, 'Epa, vamos pesquisar. eu sou info')
    # messages.warning(request, 'Epa, vamos pesquisar. eu sou warning')

    # Usando a função de Paginação
    page_obj, paginacao_range = make_pagination(request, recipes, PER_PAGES)

    return render(request, 'recipes/pages/home.html', status=200, context={
        'name': name_of_site,
        # 'recipes': [make_recipe() for _ in range(3)],
        'recipes': page_obj,
        'paginacao_range': paginacao_range,
        'show': 1,
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

    page_obj, paginacao_range = make_pagination(request, recipes, PER_PAGES)

    return render(request, 'recipes/pages/category.html', context={
        'name': name_of_site,
        'title': f'{recipes[0].category.name} | Recipes',
        'recipes': page_obj,
        'paginacao_range': paginacao_range
    })


def recipe(request, id):
    '''recipe = Recipes.objects.filter(
        pk=id,
        ).order_by('-id').first()'''
    # Simplificando o código acima, com a Função get_object_or_404
    recipe = get_object_or_404(Recipes, pk=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'name': name_of_site,
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
    # Aqui estamos pegando o valor procurando, como coloquei o nome de Q, recebo o mesmo aqui. # noqa: 501
    search_term = request.GET.get('q', '').strip()
    consultando_receitas = Recipes.objects.filter(
        # Colocando = ele vai procurar o termo exatamente igual oque não é interessante. # noqa: 501
        # title=search_term,
        # Onde a ideia seria usar o termo de Like no sql, segue exemplo de como funcionaria. # noqa: 501
        # Para procurar o termo independentemente se há letras maiúsculas ou minúsculas, coloque um i na frente de contains. # noqa: 501
        # O método usado abaixo equivale a procura por termos com ou (OR) ao invés de E (AND) # noqa: 501
        # Quando envolvemos o Ou todo por um Q podemos também colocar a condicional E da seguinte forma. # noqa: 501
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True,
        # Colocando um order pelo ID para pegar as receitas que foram criados por último, ou seja mais recentes. # noqa: 501
    ).order_by('-pk')

    print(f' Procurado por {search_term} em {consultando_receitas}')

    if not search_term:
        raise Http404()

    page_obj, paginacao_range = make_pagination(request, consultando_receitas, PER_PAGES)  # noqa: 501

    return render(request, 'recipes/pages/search.html', {
        # O par de Chaves é o valor que a Página está esperando receber, e o valor é a variável definida nessa função. # noqa: 501
        'recipes': page_obj,
        'search_term': search_term,
        'name': name_of_site,
        'page_title': f'Resultados para {search_term} no site ',
        'paginacao_range': paginacao_range,
        'additional_url_query': f'&q={search_term}',
    })
    # atualizando
