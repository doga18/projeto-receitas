from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


# Funções para simplificar.
def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    # Usando uma função baseado na de cima.
    add_attr(field, 'placeholder', placeholder_val)
    # field.widget.attrs['placeholder'] = placeholder_val


def strong_password(password):
    # expressão relugar
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'A senha informada é muito curta, mínimo de 8 caracteres.',

        ),
            code='password_is_very_small',
        )


class RegisterForm(forms.ModelForm):
    # Sobreescrevendo campos
    # Esse campo não existe em User, foi criado temporariamente somente para validações. # noqa: 501
    password2 = forms.CharField(
        required=True,
        label='Confirme sua senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita sua senha',
            'label': 'Confirme sua senha',
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must has at least one uppercase letter'
            'one lower case letter and one number.'
        ),
        validators=[strong_password]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs['placeholder'] = 'adasd'
        add_placeholder(self.fields['email'], 'Insira aqui seu e-mail')
        add_placeholder(self.fields['first_name'], 'ex: Pedro')
        add_placeholder(self.fields['last_name'], 'ex: Pinheiro')        
        add_attr(self.fields['password'], 'label', 'Digite novamente sua senha.')  # noqa: 501

    # A Meta é necessária para passar meta dados para o django.
    class Meta:
        # Qual modem vamos usar, no caso o User.
        model = User
        # Quais campos vamos usar.
        # Campos
        # Usando o __all__ ele Trará todos os campos daquele model, isso é muito importante. # noqa: 501
        # fields = '__all__'
        # Especificando
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            # 'password2',
        ]
        # Do mesmo jeito que existe o __all__ para mostrar todos os campos existe o exclude, para excluir campos. # noqa: 501
        # exclude = [
        #    'first_name',
        # ]
        # Tem como também manipularmos o label que vem do model, exemplo.
        # Dando esse novo apelido para quando for importado no formulário.
        labels = {
            'username': 'Digite aqui seu usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'password': 'Senha',
            'password2': 'Confirme sua senha',
        }
        help_texts = {
            'email': 'O e-mail precisa ser válido.',
            'username': 'Não pode conter espaços.',
        }
        error_messages = {
            'username': {
                'required': 'Este campo não pode ser vazio.',
            }
        }
        widgets = {
            # charfield
            'username': forms.TextInput(attrs={
                'placeholder': 'Insira seu usuário aqui.',
                'class': 'input outra-classe'
            }),
            # password field
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Insira sua senha',
            })
        }

    # Validações específicas por campos.
    # Clean Field Ex Abaixo.
    def clean_password(self):
        # Na Linha abaixo o data, pega da página o campo de nome password
        # Aqui onde é definido onde pegar e oque pegar.
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Valor inválido. Não digite %(value)s, neste campo.',
                # Para criar os próprios códigos da nossa aplicação.
                code='Invalid',
                params={'value': 'atenção'}
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo de Nome',
                code='Invalid',
                params={'value': '"John Doe"'},
            )

        return data

    def clean(self):
        dados_tratados = super().clean()
        first_name = dados_tratados.get('first_name')
        last_name = dados_tratados.get('last_name')
        user = dados_tratados.get('username')
        password = dados_tratados.get('password')
        password2 = dados_tratados.get('password2')

        password_dont_match = ValidationError(
            'As senhas não conferem, favor tentar novamente.',
            code='password_dont_match'
        )

        password_is_very_small = ValidationError(
            'A senha informada é muito curta, mínimo de 6 caracteres.',
            code='password_is_very_small'
        )

        password_contains_name = ValidationError(
            'A sua senha não pode conter informações sobre seu cadastro.',
            code='password_contains_name'
        )

        if password != password2:
            raise ValidationError({
                'password': password_dont_match,
                'password2': [
                    password_dont_match,
                    'As senha precisam ser idênticas, favor tentar novamente.'
                    ] # noqa: 501
            })

        if len(password) < 6:
            raise ValidationError(
                {
                    'password': password_is_very_small,
                }
            )

        if password == first_name or password == last_name or password == user:
            raise ValidationError(
                {
                    'password': password_contains_name,
                }
            )


class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User

        fields = {
            'username': 'Usuário',
        }
