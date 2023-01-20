import os

from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages

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
        form.save()
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
