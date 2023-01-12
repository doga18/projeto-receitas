from django.core.exceptions import ValidationError
from .test_recipe_base import RecipeTestBase


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
