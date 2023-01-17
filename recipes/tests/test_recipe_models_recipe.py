from django.core.exceptions import ValidationError
from .test_recipe_base import RecipeTestBase, Recipes
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'B' * 256  # Ele multiplcará B por * 70 = BBBBB...

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # Aqui que ocorre a validação.
        # self.recipe.save()
        # self.fail(len(self.recipe.title))

    def make_recipes_no_defaults(self):
        recipe = Recipes(
            category=self.make_category(name='Carnes'),
            author=self.make_author(username='Diego'),
            title='Recipe Title1',
            description='Recipe Description1',
            slug='recipe-slu1',
            preparation_time=101,
            preparation_time_unit='Minuto1s',
            servings=5,
            servings_unit='Porçõe1s',
            preparation_steps='Recipe Preparation Step1s',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 255),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65)
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        # Aqui já estou desempacotando os valores para poder comparar.
        # for field, max_length in fields:            
        setattr(self.recipe, field, 'A' * (max_length + 0))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_step_is_html_is_false_by_default(self):
        recipe = self.make_recipes_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparations is not False, eu mesmo escrevi.',
        )
        
