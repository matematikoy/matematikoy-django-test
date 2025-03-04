from django.contrib import admin
from .models import Post, Category, Comment  # Adicione o Comment aqui

# Personalizando o admin para o Post
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'category', 'picture',)
    search_fields = ('title', 'content')

# Registrando o modelo Post com a personalização
admin.site.register(Post, PostAdmin)

# Registrando o modelo Category (sem personalização)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']

# Personalizando o admin para o Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'post', 'user', 'created_at', 'likes')  # Campos que aparecerão na lista
    search_fields = ('comment', 'post__title', 'user__username')  # Permite busca pelos campos de comentário, post e usuário

# Registrando o modelo Comment com a personalização
admin.site.register(Comment, CommentAdmin)
