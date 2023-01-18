import os

from django.http import Http404
from django.shortcuts import redirect, render

from .forms import RegisterForm

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
    form = RegisterForm(request.POST)  # noqa: F841

    print(request.session['register_form_data'])

    return redirect('authors:register')
