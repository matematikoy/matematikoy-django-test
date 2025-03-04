
from django.urls import path
from .views import CommentHandler  # Importando a view onde o comentário é processado
from . import views

urlpatterns = [
    path('', views.index ),
    path('login/', views.login_view),
    path('signup/', views.signup_view),
    path('logout', views.logout_view),
    path('categorys/', views.CategoryHandler.see_categorys_view),
    path('trending/', views.trending_view),
    path('<str:category_name>/', views.category_view, name='category_view'),
    path('api/comentarios/adicionar/', CommentHandler.comment_post_view, name='adicionar_comentario'),
    path('like/post/<int:post_id>/', views.PostHandler.add_like_post, name='add_like_post'),
    path('like/comment/<int:comment_id>/', views.CommentHandler.add_like_comment, name='add_like_comment'),
    

]
