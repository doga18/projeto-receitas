import os

from django.http import Http404
from django.shortcuts import redirect, render 
from django.contrib import messages
from django.urls import reverse

from .forms import RegisterForm, LoginForm

# Nome do Site.
name_of_site = os.environ.get('NAME_OF_SITE')


def register_view(request):
    # Aqui estão exemplos de como pegar dados de sessão.
    # request.session['number'] = request.session.get('number') or 1
    # request.session['number'] += 1
    # valor_session = request.session['number']
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', status=200, context={  # noqa: 501
        'name': name_of_site,
        'form': form,
        'form_action': reverse('authors:create'),

    })


def register_create(request):
    # Verificamos se existem dados Post vindo dessa página, se sim, faça tal coisa. # noqa: 501
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)  # noqa: F841

    print(request.session['register_form_data'])

    if form.is_valid():
        # Este exemplo, mas com que 'Seguremos os dados do form' para fazer algo. # noqa: 501
        # Ele finge que salva, mas não commit, então não salva.
        # Isso serve para quando você precisa, definir algum valor também à mais antes de salvar de fato. # noqa: 501
        # Ex
        # dados_salvos = form.save(commit=False)
        # Lembre-se que o commit=False serve para você tratar os dados que vieram antes de salvar. # noqa: 501
        # form.save(commit=False)
        # Determinando o save a uma variável para trabalhar esses dados.
        user = form.save(commit=False)
        # O user.password vem como String.
        # O set_password é uma função de criptografar a senha, após isso, salvamos. # noqa: 501
        user.set_password(user.password)
        
        # Salvo de fato.
        user.save()
        messages.success(request, 'Seu cadastro foi realizado com sucesso, agora Realize seu Login') # noqa: 501

        # Limpar os dados do formulário.
        del (request.session['register_form_data'])
        # Após o cadastro, podemos voltar para o Login.

    return redirect('authors:register')


def do_login(request):
    # if not request.POST:
    #    raise Http404()

    POST = request.POST
    request.session['login_form_data'] = POST
    login_form = LoginForm(POST)

    return render(request, 'authors/pages/login_view.html', context={
        'name': 'Efetue seu Login',
        'form': login_form
    })
