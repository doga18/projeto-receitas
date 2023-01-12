from django.test import TestCase
from recipes.models import Category, Recipes, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        # Isso setamos na mão
        # category = Category.objects.create(name='Category')
        # Para usarmos um método, usamos da seguinte forma.
        # category = self.make_category(name='Categoria Carnes')
        # Se eu deixar o make_recipe aqui, essa função, e chamar ela nos testes que eu preciso, ele criará os dados duas vezes. # noqa: 501
        # E Como tem dados que são criados únicos é provável que dará problemas, por isso, deixamos aqui somente quando formos rodar o teste direto aqui: # noqa: 501
        # self.make_recipe()
        return super().setUp()

    # Funciona da seguinte forma, se eu não passar nada para nome ele usa o default que é o "Nome_da_categoria" # noqa: 501
    def make_category(self, name='Nome_da_categoria'):
        return Category.objects.create(name=name)

    # Mesma ideia, se não passar os dados para cada um dos campos, ele usará os padrões, se passar usa oque foi informado # noqa: 501
    def make_author(
        self,
        first_name='user_padrao',
        last_name='ultimo_nome_padrao',
        username='username_padrao',
        password='password_padrao',
        email='email_padrao@gmail.com'
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Recipe Description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutos',
        servings=5,
        servings_unit='Porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipes.objects.create(
            # Os ** serve para desempacotar a lista com suas chaves, essa variável tem chave e valor (name='valor) # noqa: 501
            # Ao desempacotar, enviamos o name e o valor de name que é 'valor'
            # Se eu não desempacoto, eu estou enviando o objeto lista ao invés do valor solicitado. # noqa: 501
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,  
        )


# Exemplo sem os métodos
'''class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = Recipes.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        return super().setUp()
        '''
