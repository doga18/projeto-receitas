from django.urls import path
from authors import views

# Name of App
app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),
    path('login/', views.do_login, name='login'),
]
