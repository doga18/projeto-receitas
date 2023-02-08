from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.test import TestCase as DjangoTestCase
from django.urls import reverse


class AuthorRegisterFormUnitest(TestCase):
    # O parameterized, ele testa campo por campo, sem quebrar o test, mesmo que 1 falhe. # noqa: 501
    @parameterized.expand([
        ('username', 'Insira seu usuário aqui.'),
        ('email', 'Insira aqui seu e-mail'),
        ('first_name', 'ex: Pedro'),
        ('last_name', 'ex: Pinheiro'),
        ('password', 'Insira sua senha ex: Abc123456'),
        ('password2', 'Repita sua senha ex: Abc123456'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_place_holder = form[field].field.widget.attrs['placeholder']
        print(f'Este é o placeholder {current_place_holder} que é visto pelo field, esse é o {placeholder} comparado.') # noqa: 501
        self.assertEqual(current_place_holder, placeholder)

    @parameterized.expand([
        ('password2', (
            'Password must has at least one uppercase letter',
            'one lower case letter and one number.')),
        ('email', 'O e-mail precisa ser válido.'),
        ('username', 'Não pode conter espaços.'),
    ])
    def test_fields_helptext_is_correct(self, field, helptext):
        form = RegisterForm()
        current_helptext = form[field].field.help_text
        print(current_helptext, helptext)
        self.assertEqual(current_helptext, helptext)

    @parameterized.expand([
        ('username', 'Digite aqui seu usuário'),
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('email', 'Email'),
        ('password', 'Senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_fields_label(self, field, helptext):
        form = RegisterForm()
        current_helptext = form[field].field.label
        print(current_helptext, helptext)
        self.assertEqual(current_helptext, helptext)


class AuthorRegisterFromIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',

        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Este campo é obrigatório'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('author:create')
        response = self.cliente.post(url, data=self.form_data)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_email_if_already_exists(self):
        url = reverse('authors:create')

        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'User e-mail is already registered'

        self.assertIn(msg, response.context['form'].errors.get('email'))  # noqa: 501
        self.assertIn(msg, response.content.decode('utf-8'))
