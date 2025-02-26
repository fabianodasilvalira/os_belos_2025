from rest_framework import serializers
from .models import Post, Comment, Like


# Serializer para Curtidas
class LikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')  # Incluindo o nome de usuário na curtida

    class Meta:
        model = Like
        fields = ['user_name', 'created_at']  # Campos que você deseja retornar para as curtidas


# Serializer para Comentários
class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', default='Usuário Desconhecido')

    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'content', 'created_at']

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M:%S')  # Formato brasileiro


# Serializer para Post
class PostSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)  # Incluindo as curtidas do post

    class Meta:
        model = Post
        fields = ['id', 'user_name', 'title', 'content', 'image', 'video', 'created_at', 'updated_at', 'comments',
                  'likes']

    def get_user_name(self, obj):
        return obj.user.username if obj.user else 'Usuário Desconhecido'

    def get_created_at(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M:%S')

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%d/%m/%Y %H:%M:%S')
