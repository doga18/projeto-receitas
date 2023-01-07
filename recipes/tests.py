from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    '''def test_the_pytest_is_ok(self):
        assert 1 == 1, 'Um é igual a um'''

    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEquals(home_url, '/')

    def test_recipe_category_url_is_correct(self):
        # Exemplo de mandar com o value direto.
        # url = reverse('recipes:category', args=(1,))
        # Exemplo de mandar com a lista
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEquals(url, '/')