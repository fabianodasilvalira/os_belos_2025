from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from social.views import LoginView, LogoutView

urlpatterns = [
    # Suas outras rotas...
    path('admin/', admin.site.urls),
    path('api/', include('social.urls')),  # Corrigido parêntese
    path('api/login/', LoginView.as_view(), name='login'),
    # Rota para logout (excluir o token)
    path('api/logout/', LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
