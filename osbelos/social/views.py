from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Comment, Like, Reaction
from .serializers import PostSerializer, CommentSerializer, ReactionSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import Http404, FileResponse, JsonResponse
from django.conf import settings
from rest_framework.views import APIView
import os


# LOGIN (Gerar Token JWT)
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
                'access_token': access_token,  # Retorna o token de acesso
                'refresh_token': str(refresh)  # Retorna também o refresh token
            }, status=status.HTTP_200_OK)

            # Configura o cookie com o token de acesso (para JWT)
            response.set_cookie(
                'access_token', access_token,
                httponly=True,  # Para evitar acesso ao cookie via JavaScript
                secure=True,  # Defina como True em produção
                samesite='Strict'
            )
            return response

        # Se o usuário ou a senha estiverem errados
        return Response({"detail": "Usuário ou senha inválidos!"}, status=status.HTTP_400_BAD_REQUEST)


# LOGOUT (Invalidar Token JWT)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"detail": "Refresh token não fornecido!"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalida o token

            return Response({"message": "Usuário deslogado com sucesso!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# POSTS (CRUD de postagens)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem criar posts

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)  # Salva o post com o user (ou None se não autenticado)

    # Curtir ou descurtir postagens
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

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

    # Acessar arquivos de mídia protegidos
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def media(self, request, pk=None):
        post = self.get_object()

        # Verifica o tipo de mídia e retorna o arquivo correspondente
        if post.image:
            file_path = os.path.join(settings.MEDIA_ROOT, post.image.name)
        elif post.video:
            file_path = os.path.join(settings.MEDIA_ROOT, post.video.name)
        else:
            raise Http404("Mídia não encontrada!")

        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            raise Http404("Arquivo não encontrado!")

        # Retorna o arquivo de mídia de forma segura
        with open(file_path, 'rb') as file:
            return FileResponse(file)


# COMENTÁRIOS (CRUD de comentários)
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


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar esta rota

    def get(self, request):
        # Recupera o usuário autenticado
        user = request.user
        # Retorna os dados do usuário em formato JSON
        return Response({
            'id': user.id,
            'username': user.username,
        })


class ReactToCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        reaction_type = request.data.get('reaction_type')

        # Verifica se o tipo de reação é válido
        if reaction_type not in dict(Reaction.REACTION_TYPES):
            return Response({'error': 'Reação inválida'}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o usuário já reagiu ao comentário
        reaction, created = Reaction.objects.get_or_create(
            user=request.user, comment=comment, reaction_type=reaction_type
        )

        # Se o usuário já tiver reagido ao comentário com o mesmo tipo, exclui a reação
        if not created:
            reaction.delete()
            return Response({'message': 'Reação removida'}, status=status.HTTP_200_OK)

        # Retorna a reação criada
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)