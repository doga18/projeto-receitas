from recipes.models import Recipes
from django.urls import reverse
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewsTest(RecipeTestBase):
    def test_recipe_home_view_returns_status_code_200_OK(self):
        # Na consulta abaixo, emulamos um cliente, para buscar informações em um site "get" # noqa: 501
        # E jogamos isso para uma variável para ver a resposta.
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        # Na consulta abaixo, emulamos um cliente, para buscar informações em um site "get" # noqa: 501
        # E jogamos isso para uma variável para ver a resposta.
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

        # @skip('WIP') Para pular testes.
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        # Como o setup, cria aquela receita para todos os testes, e esse teste
        # precisa que não exista receita, quando entrar nesse testa a linha abaixo # noqa: 501
        # Deleta essa receita para que esse teste comece sem receita.
        # Lembrando que todos os setUP e TearDown são isolados por test.
        # Essas duas linhas abaixo não são necessárias, mas deixei para melhor compreensão # noqa: 501
        # O Make abaixo cria os dados dos testes.
        self.make_recipe()
        # O comando abaixo deleta a Receita criada com o id 1.
        Recipes.objects.get(pk=1).delete()
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h2>Sem Receitas Cadastradas no momento.</h2>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # Enviando dados, mas isso irá quebrar se a comparação abaixo não estiver comparando com os valores informados aqui. # noqa? 501
        # self.make_recipe(preparation_time=18, preparation_time_unit='Minutos') # noqa: 501
        self.make_recipe(author_data={
            'username': 'joaozinho'
        }, category_data={
            'name': 'Carnes'
        })
        response = self.client.get(reverse('recipes:home'))
        # Onde o content é o conteúdo que vai receber o valor da html realizado decode # noqa: 501
        content = response.content.decode('utf-8')
        # Verificando se no HTML recebido (Que simula a navegação no site.) Se foi renderizado tal String procurada, exemplo as informações criadas acima. # noqa: 501
        self.assertIn('Recipe Title', content)
        # Verificando se 10 minutos existe na renderização.
        self.assertIn('10 Minutos', content)
        # Verificando se existe 5 Porções, atente-se que é na verificação CaseSensitive # noqa: 501
        self.assertIn('5 Porções', content)
        # Verificando se existe o author declarado acima.
        self.assertIn('joaozinho', content)
        self.assertIn('Carnes', content)        
        # Após criar a receita acima, podemos ver quantas receitas foram criadas # noqa: 501
        # Como Criamos somente uma, se usarmos a função len, deverá mostrar
        # somente 1
        response_context_recipes = response.context['recipes']
        self.assertEqual(len(response_context_recipes), 1)
        pass

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        # Esse teste, vê se o is_published for false não mostre.
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h2>Sem Receitas Cadastradas no momento.</h2>',
            response.content.decode('utf-8')
        )

    # O Patch serve para pegar um valor de uma variável global, alterar o valor dela para o teste e depois voltar o valor dela que estava antes. # noqa: 501
    # Assim ao alterar o valor, não quebra os demais testes. # noqa: 501
    # Esse é o modo usando decorator.
    # @patch('recipes.views.PER_PAGES', new=3)
    def test_recipe_home_is_paginated(self):

        # Esse teste, vê se o is_published for false não mostre.
        for i in range(9):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        # Aqui seria o teste via With.
        with patch('recipes.views.PER_PAGES', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1), 3))
            self.assertEqual(len(paginator.get_page(2), 3))
            self.assertEqual(len(paginator.get_page(3), 2))            

    def test_recipe_search_can_find_recipe_by_title(self):
        title_1 = 'This is recipes one'
        title_2 = 'This is recipes two'

        recipe_1 = self.make_recipe(
            slug='one',
            title=title_1,
            author_data={'username': 'one'}
        )

        recipe_2 = self.make_recipe(
            slug='two',
            title=title_2,
            author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response_1 = self.client.get(f'{search_url}?q={title_1}')
        response_2 = self.client.get(f'{search_url}?q={title_2}')
        response_both = self.client.get(f'{search_url}?q=this')
        print(response_1, response_2, response_both, recipe_1, recipe_1, recipe_2) # noqa: 501
