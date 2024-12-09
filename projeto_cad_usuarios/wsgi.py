import os
import sys

# Adicione o caminho do diretório do projeto
path = '/home/niltinho/ProjetoCadastro'  # Atualize com o caminho correto do seu projeto
if path not in sys.path:
    sys.path.append(path)

# Defina o módulo de configurações
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_cad_usuarios.settings')

# Ative a aplicação WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
