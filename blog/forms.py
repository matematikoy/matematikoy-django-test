from django import forms
from .models import Post, Category, Comment

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):

    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'picture']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'picture']

    picture = forms.ImageField(required=False)

class CreateCategory(forms.Form):
    
    category_name = forms.CharField(max_length=100)
