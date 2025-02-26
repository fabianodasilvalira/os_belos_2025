from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Autentica o usuário
        user = authenticate(username=username, password=password)
        if user:
            # Gera o refresh token (corrigido para usar simplejwt)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Cria a resposta com o token
            response = Response({
                'message': 'Login bem-sucedido',
                'access_token': access_token  # Retorna o token de acesso
            }, status=status.HTTP_200_OK)

            # Configura o cookie com o token de acesso (para JWT)
            response.set_cookie(
                'access_token', access_token,
                httponly=True,  # Para evitar acesso ao cookie via JavaScript
                secure=True,    # Defina como True em produção
                samesite='Strict'
            )
            return response

        # Se o usuário ou a senha estiverem errados
        return Response({"detail": "Usuário ou senha inválidos!"}, status=status.HTTP_400_BAD_REQUEST)


# Logout (Deletar Token)
class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Deleta o token do usuário, efetivamente realizando o logout
        request.user.auth_token.delete()
        return Response({"message": "Usuário deslogado com sucesso!"})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem criar posts

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)  # Salva o post com o user (ou None se não autenticado)

    # Action para curtir e descurtir postagens
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])  # Permite curtir sem autenticação
    def like(self, request, pk=None):
        post = self.get_object()

        # Permitir que qualquer pessoa curta, mesmo sem estar autenticada
        user = request.user if request.user.is_authenticated else None

        if user is None:
            return Response({"detail": "Usuário não autenticado!"}, status=status.HTTP_401_UNAUTHORIZED)

        # Verifica se o usuário já curtiu o post
        existing_like = Like.objects.filter(user=user, post=post).first()

        if existing_like:
            # Se o usuário já curtiu, descurte
            existing_like.delete()
            return Response({"message": "Post descurtido!"}, status=status.HTTP_200_OK)
        else:
            # Se o usuário ainda não curtiu, cria o like
            Like.objects.create(user=user, post=post)
            return Response({"message": "Post curtido!"}, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem comentar

    def get_queryset(self):
        # Filtra os comentários pelo post_id, se fornecido
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post_id', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset
