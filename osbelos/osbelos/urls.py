from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from social import views
from social.views import LoginView, LogoutView, CurrentUserView, ReactToCommentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('social.urls')),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/current_user/', CurrentUserView.as_view(), name='current_user'),
    path('api/comments/<int:comment_id>/react/', ReactToCommentView.as_view(), name='react_to_comment'),
    path('accounts/', include('allauth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
