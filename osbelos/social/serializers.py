from rest_framework import serializers
from .models import Post, Comment, Like, Reaction


# Serializer para Curtidas
class LikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')  # Incluindo o nome de usuário na curtida

    class Meta:
        model = Like
        fields = ['user_name', 'created_at']  # Campos que você deseja retornar para as curtidas


# Serializer para Comentários
from rest_framework import serializers
from .models import Comment, Post

class CommentSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)  # Definido como IntegerField

    class Meta:
        model = Comment
        fields = ["id", "post_id", "user", "content", "created_at"]

    def create(self, validated_data):
        post_id = validated_data.pop("post_id")
        post = Post.objects.get(id=post_id)  # Busca o post correspondente
        comment = Comment.objects.create(post=post, **validated_data)  # Cria o comentário associado ao post
        return comment



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


# social/serializers.py
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['id', 'user', 'comment', 'reaction_type', 'created_at']

