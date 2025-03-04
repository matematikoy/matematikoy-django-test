from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    picture = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)  # Usuários que curtiram
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Chave estrangeira com User
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Chave estrangeira com Categoria
    
    def __str__(self):
        return self.title


class Comment(models.Model):    
    
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)  # Relaciona o comentário com o post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o comentário com o usuário
    comment = models.TextField()
    picture = models.ImageField(upload_to='comment_uploads/%Y/%m/%d/', null=True, blank=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_comments", blank=True)  # Registra usuários que curtiram
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.user.username} em {self.post.title}"