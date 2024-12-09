from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario
from django.db.models import Avg

import pandas as pd

# Create your views here.
def home(request):
    return render(request, 'usuarios/cadastro.html')


def usuarios(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')

        # Verificar se os campos foram preenchidos
        if nome and idade:
            novo_usuario = Usuario(nome=nome, idade=idade)
            novo_usuario.save()
            return redirect('listar_usuarios')  # Redireciona após salvar
        else:
            # Retorna uma mensagem de erro se os campos estiverem vazios
            return render(request, 'usuarios/usuarios.html', {
                'error': 'Preencha todos os campos antes de salvar.'
            })

    # Exibir a listagem de usuários
    usuarios = {'usuarios': Usuario.objects.all()}
    return render(request, 'usuarios/usuarios.html', usuarios)


def editar_usuarios(request, id):
    # Obter o usuário pelo ID ou retornar 404 se não encontrado
    usuario = get_object_or_404(Usuario, id_usuario=id)

    if request.method == 'POST':
        # Atualizar os campos com os valores enviados pelo formulário
        usuario.nome = request.POST.get('nome')
        usuario.idade = request.POST.get('idade')
        usuario.save()  # Salvar alterações no banco de dados

        # Redirecionar para a página de listagem de usuários após a edição
        return redirect('listar_usuarios')  # Substitua pela URL correta

    # Renderizar a página de edição com os dados do usuário
    return render(request, 'usuarios/editar.html', {'usuario': usuario})


def excluir_usuarios(request, id):
    # Obter o usuário pelo ID ou retornar 404 se não encontrado
    usuario = get_object_or_404(Usuario, id_usuario=id)

    # Excluir o usuário
    usuario.delete()

    # Redirecionar para a página de listagem de usuários após a exclusão
    return redirect('listar_usuarios')  # Substitua pela URL correta


def grafico_idades(request):
    # Calcula a média das idades
    media_idade = Usuario.objects.aggregate(media=Avg('idade'))['media']

    # Obtem os nomes e idades dos usuários
    usuarios = Usuario.objects.values('nome', 'idade')  # Lista de dicionários

    # Renderiza os dados no template
    context = {
        'media_idade': media_idade,
        'usuarios': list(usuarios),  # Converte QuerySet para lista
    }
    return render(request, 'usuarios/grafico.html', context)


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/usuarios.html', {'usuarios': usuarios})


def importar_excel(request):
    if request.method == 'POST':
        # Verifique se o arquivo foi enviado
        if 'arquivo' not in request.FILES:
            return render(request, 'usuarios/importar.html', {'erro': 'Nenhum arquivo foi enviado.'})

        arquivo_excel = request.FILES['arquivo']

        try:
            # Ler o arquivo Excel
            df = pd.read_excel(arquivo_excel)

            # Iterar sobre os registros do DataFrame
            for _, row in df.iterrows():
                usuario, created = Usuario.objects.update_or_create(
                    id_usuario=row['id_usuario'],
                    defaults={
                        'nome': row['nome'],
                        'idade': row['idade']
                    }
                )

            return redirect('listar_usuarios')

        except Exception as e:
            return render(request, 'usuarios/importar.html', {'erro': str(e)})

    return render(request, 'usuarios/importar.html')
