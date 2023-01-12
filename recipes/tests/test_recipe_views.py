# Para pular o test.
from unittest import skip

from django.urls import resolve, reverse
from recipes import views
from recipes.models import Recipes

from .test_recipe_base import RecipeTestBase

# Como Rodar, no terminal, python manage.py test
# Para Verbose, set v1, v2 ,v3 maior, mais info python manage.py test -v2
# Para rodar teste específico, python manage.py test -k 'nome_da_function_test'


class RecipeViewsTest(RecipeTestBase):
    def tearDown(self) -> None:
        return super().tearDown()

    # Exemplos de Uso
    # SetUP
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)
    # E ao Final
    # TearDown

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1}),
        )
        self.assertIs(view.func, views.recipe)

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

    @skip('This test are Skipped')
    def para_deixar_em_uso_skip(self):
        ...

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

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 10000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        # Esse teste, vê se o is_published for false não mostre.
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_recipe_template_dont_load_recipes_not_published(self):
        # Esse teste, vê se o is_published for false não mostre.
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': recipe.id}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        # Enviando dados, mas isso irá quebrar se a comparação abaixo não estiver comparando com os valores informados aqui. # noqa? 501
        # self.make_recipe(preparation_time=18, preparation_time_unit='Minutos') # noqa: 501
        # Determinando o Title a uma variável para depois jogar no make_recipe.
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        # Onde o content é o conteúdo que vai receber o valor da html realizado decode # noqa: 501
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if category contains that name give on make_recipe with category. # noqa: 501
        self.assertIn(needed_title, content)
        # Check if a recipe is only one, with a function Equals. # noqa: 501
        self.assertEquals(len(response_context_recipes), 1)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1221})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        # Enviando dados, mas isso irá quebrar se a comparação abaixo não estiver comparando com os valores informados aqui. # noqa? 501
        # self.make_recipe(preparation_time=18, preparation_time_unit='Minutos') # noqa: 501
        # Determinando o Title a uma variável para depois jogar no make_recipe.
        needed_title = 'This is a detail page - It load one recipe'

        # É preciso uma receita para esse test.
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'id': 1}
            )
        )
        # Onde o content é o conteúdo que vai receber o valor da html realizado decode # noqa: 501
        content = response.content.decode('utf-8')

        # Check if category contains that name give on make_recipe with category. # noqa: 501
        self.assertIn(needed_title, content)
        # Check if a recipe is only one, with a function Equals. # noqa: 501
