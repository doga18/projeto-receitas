from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Create my models here.


class Category(models.Model):
    name = models.CharField(max_length=65)

    # Isso serve para que toda vez que alguém chamar essa classe ele rode esse
    # Init, neste método mágico, ele retornará o nome.
    # Para teste, Comente a parte abaixo e veja a página admin.

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(
        max_length=65, blank=True, default='Sem Author')
    last_name = models.CharField(max_length=65, blank=True)
    email = models.EmailField(max_length=254, blank=True)


class Recipes(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=165)
    slug = models.SlugField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/',
        blank=True,
        default='',
    )
    # Criando as relações de Class (Tabelas)
    # Essa Coluna, category, tem ligação com a Tabela (class) Category.
    # Note que são duas coisas diferentes porém são ligadas.
    # Explicação: On_delete é prevenção de um evento, se uma receita de pães
    # que pertente a categoria café da manhã for deletada, ao ser deletada,
    # o on_delete diz que quando deletado set null nessa coluna, e a opção de
    # Null=True, permite que tal coluna set a informação null.
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    # Essa função retorna a String do Titulo, se fosse uma pessoa,
    #  seria o name.
    def __str__(self):
        return self.title
