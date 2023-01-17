# Para pular o test.
from unittest import skip

from django.urls import resolve, reverse
from recipes import views
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

    @skip('This test are Skipped')
    def para_deixar_em_uso_skip(self):
        ...

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

    def teste_recipe_search_url_is_correct(self):
        # Podemos simplificar as linhas abaixo, colocando tudo isso em uma variável, segue exemplo # noqa: 501
        # url = reverse('recipes:search')
        # self.assertEquals(url, '/recipes/search/')
        # Fazer falhar e mostrar a variável URL
        # self.fail(url)
        url_resolvida = resolve(reverse('recipes:search'))
        self.assertIs(url_resolvida.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        resposta = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(resposta, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        # Aqui colocamos uma string a mais no teste para fazer o teste de fato falhar. # noqa: 501
        # url = reverse('recipes:search') + '?q=teste'
        response = self.client.get(reverse('recipes:search'))
        # response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):        
        url = reverse('recipes:search') + '?q=qa'
        response = self.client.get(url)
        self.assertIn(
            'Resultados para qa no site ',
            response.content.decode('utf8'),
        )
