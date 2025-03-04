from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, PostForm, CreateCategory, CommentForm
from .models import Post, Category, Comment
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateformat import format



class PostHandler:

    @staticmethod
    def create_post_view(request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/')
        
    def add_like_post(request, post_id):
        if request.method == "POST":
            post = get_object_or_404(Post, id=post_id)
            user = request.user  

            if user in post.liked_by.all():  # Verifica se o usuário já curtiu
                post.liked_by.remove(user)  # Remove o like
                post.likes -= 1
                post.save()
                return JsonResponse({'success': True, 'likes': post.likes, 'liked': False})

            post.liked_by.add(user)  # Adiciona o usuário à lista de curtidas
            post.likes += 1
            post.save()

            return JsonResponse({'success': True, 'likes': post.likes, 'liked': True})

        return JsonResponse({'success': False, 'error': 'Método inválido'}, status=400)
        


        
class CategoryHandler:

    @staticmethod

    def create_category_view(request):

        if request.user.has_perm('blog.add_category'):
            category_form = CreateCategory(request.POST)
            if category_form.is_valid():
                category_name = category_form.cleaned_data['category_name']
                Category.objects.create(category_name=category_name)
                return redirect('/')
            
            

    def see_categorys_view(request):
        categorys = Category.objects.all()
        return render(request, 'blog/categorys.html', {'categorys': categorys})        



        
     

class CommentHandler:

    @staticmethod
    @csrf_exempt
    def comment_post_view(request):
        if request.method == 'POST':
            print("🔍 Recebendo dados:", request.POST, request.FILES)  # Debug

            try:
                comment_text = request.POST.get('comment')
                post_id = request.POST.get('post_id')
                picture = request.FILES.get('picture')  # Agora deve funcionar!

                if not post_id:
                    return JsonResponse({'error': 'ID do post não enviado'}, status=400)

                try:
                    post_id = int(post_id)  
                    post = Post.objects.get(id=post_id)  
                except ValueError:
                    return JsonResponse({'error': 'ID do post inválido'}, status=400)
                except Post.DoesNotExist:
                    return JsonResponse({'error': 'Post não encontrado'}, status=404)

                comment = Comment(post=post, user=request.user, comment=comment_text, picture=picture)
                comment.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Comentário enviado com sucesso!',
                    'comment': {
                        'id': comment.id,
                        'user': comment.user.username,
                        'comment': comment.comment,
                        'created_at': format(comment.created_at, "j \\d\\e F \\d\\e Y \\à\\s H:i"),
                        'likes': comment.likes,
                        'picture_url': comment.picture.url if comment.picture else None
                    }
                })

            except Exception as e:
                print("Erro na view:", str(e))
                return JsonResponse({'error': 'Erro interno no servidor'}, status=500)

        return JsonResponse({'error': 'Método não permitido'}, status=405)

    def add_like_comment(request, comment_id):
        if request.method == "POST":
            comment = get_object_or_404(Comment, id=comment_id)
            user = request.user  

            if user in comment.liked_by.all():  # Verifica se o usuário já curtiu
                comment.liked_by.remove(user)  # Remove o like
                comment.likes -= 1
                liked = False  # Define o status para não curtido
            else:
                comment.liked_by.add(user)  # Adiciona o like
                comment.likes += 1
                liked = True  # Define o status para curtido
            
            comment.save()

            return JsonResponse({
                'success': True,
                'likes': comment.likes,
                'liked': liked  # Adiciona o status do like
            })

        return JsonResponse({'success': False, 'error': 'Método inválido'}, status=400)
    
    

def category_view(request, category_name):

    if request.method == 'POST':
        
        return CommentHandler.comment_post_view(request)

    else:
        comment_form = CommentForm()  

    comment_form = CommentForm()  
    category = get_object_or_404(Category, category_name=category_name) 
    posts = Post.objects.filter(category=category).order_by('-published_at')

    return render(request, 'blog/category_view.html', {'category': category, 'posts': posts, 'comment_form': comment_form})

def trending_view(request):
    category_form = CreateCategory()
    form = PostForm()
    comment_form = CommentForm()
    posts = Post.objects.all().order_by('-likes')  # Ordena do mais votado para o menos votado

    if request.method == 'POST':
        if 'create_post' in request.POST:
            return PostHandler.create_post_view(request)
            
        elif 'comment_post' in request.POST:
            return CommentHandler.comment_post_view(request)
            
        elif 'create_category' in request.POST:

            return CategoryHandler.create_category_view(request)
                
    return render(request, 'blog/trending.html', {'form': form, 'category_form': category_form, 'posts': posts, 'comment_form': comment_form})


    

@login_required
def index(request):


    category_form = CreateCategory()
    form = PostForm()
    comment_form = CommentForm()
    posts = Post.objects.order_by('-published_at')  # Ordena do mais recente para o mais antigo

    if request.method == 'POST':
        if 'create_post' in request.POST:
            return PostHandler.create_post_view(request)
            
        elif 'comment_post' in request.POST:
            return CommentHandler.comment_post_view(request)
            
        elif 'create_category' in request.POST:

            return CategoryHandler.create_category_view(request)
                
    return render(request, 'blog/index.html', {'form': form, 'category_form': category_form, 'posts': posts, 'comment_form': comment_form})


def login_view(request):

    if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')  # Redirecionar para a página inicial após o login
                else:
                    form.add_error(None, 'Usuário ou senha inválidos')  # Adiciona uma mensagem de erro
    else:
        form = LoginForm()
        
    return render(request, 'blog/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Criação do usuário com a senha criptografada
            user = User.objects.create_user(username=username, password=password)


            # Redireciona para a página inicial ou outra página desejada após o login
            return redirect('/login/')  # Ou qualquer outra URL que você preferir

        else:
            form.add_error(None, 'Erro ao criar a conta.')
    else:
        form = SignupForm()

    return render(request, 'blog/signup.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')



