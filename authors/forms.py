from django import forms
from django.contrib.auth.models import User


# Funções para simplificar.
def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    # Usando uma função baseado na de cima.
    add_attr(field, 'placeholder', placeholder_val)
    # field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs['placeholder'] = 'adasd'
        add_placeholder(self.fields['email'], 'Insira aqui seu e-mail')
        add_attr(self.fields['password2'], 'label', 'Digite novamente sua senha.')  # noqa: 501

    # Sobreescrevendo campos
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repita sua senha',
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must has at least one uppercase letter'
            'one lower case letter and one number.'
        )
    )

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
        ]
        # Do mesmo jeito que existe o __all__ para mostrar todos os campos existe o exclude, para excluir campos. # noqa: 501
        # exclude = [
        #    'first_name',
        # ]
        # Tem como também manipularmos o label que vem do model, exemplo.
        # Dando esse novo apelido para quando for importado no formulário.
        labels = {
            'username': 'Digite aqui seu usuário',
            'first_name': 'Seu nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'password': 'Senha',
            'password2': 'Confirme sua senha',
        }
        help_texts = {
            'email': 'The e-mail must be a email valid.'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
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
