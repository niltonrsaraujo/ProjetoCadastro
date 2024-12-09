"""
URL configuration for projeto_cad_usuarios project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_cad_usuarios import views


urlpatterns = [
    path('admin/', admin.site.urls),

    #Rota, View responsável + Função, Nome de referência
    # Rota para o cadastro de usuários
    path('', views.home, name='cadastro_usuarios'),

    # Listagem de usuários
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),

    # Edição de usuário
    path('usuarios/<int:id>/editar/', views.editar_usuarios, name='editar_usuarios'),

    # Exclusão de usuário
    path('usuarios/<int:id>/excluir/', views.excluir_usuarios, name='excluir_usuarios'),

    # Gráfico de idades
    path('grafico/', views.grafico_idades, name='grafico_idades'),

    # Importação de Excel
    path('importar/', views.importar_excel, name='importar_usuarios'),

    #Programação Linear
    path('linear/', include('linear_app.urls'), name='linear'),
]