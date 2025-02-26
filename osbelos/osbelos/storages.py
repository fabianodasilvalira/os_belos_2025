from django.core.files.storage import FileSystemStorage
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

class AuthenticatedFileSystemStorage(FileSystemStorage):
    def _open(self, name, mode='rb'):
        # Verifica se o usuário está autenticado e autorizado a acessar o arquivo
        if not self.user_is_authenticated():
            raise PermissionDenied("Você não tem permissão para acessar esse arquivo.")
        return super()._open(name, mode)

    def user_is_authenticated(self):
        # Lógica personalizada para verificar se o usuário está autenticado
        user = get_user_model()
        # Implementar a lógica necessária para checar a autenticação
        return True  # Ajuste conforme necessário
