from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment, Like, Message, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'updated_at', 'image_preview', 'video_link', 'like_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{0}" width="100" height="100" />', obj.image.url)
        return "Sem imagem"

    image_preview.short_description = 'Imagem'

    def video_link(self, obj):
        if obj.video:
            return format_html('<a href="{0}" target="_blank">Ver vídeo</a>', obj.video.url)
        return "Sem vídeo"

    video_link.short_description = 'Vídeo'

    def like_count(self, obj):
        return obj.likes.count()

    like_count.short_description = 'Curtidas'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    search_fields = ('user__username', 'content')
    list_filter = ('created_at', 'post')
    ordering = ('-created_at',)


admin.site.register(Like)
admin.site.register(Message)
admin.site.register(Follow)
