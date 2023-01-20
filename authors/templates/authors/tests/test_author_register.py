from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import Parameterized


class AuthorRegisterFormUnitest(TestCase):
    @Parameterized.expand([
        ('username', 'Seu usuário'),
        ('email', 'Seu email'),
        ('password', 'Seu password'),
        ('first_name', 'Seu Nome'),
        ('last_name', 'Seu Sobrenome'),
        ('password2', 'Confirmar Senha'),
    ])
    def test_first_name_placeholder_is_correct(self):
        form = RegisterForm()
        field_to_verify = form['first_name'].field.widget.attrs['placeholder']
        self.assertEqual('', field_to_verify)
