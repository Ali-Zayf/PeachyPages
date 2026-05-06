from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post, Comment
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404
from django.db.models import Q

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post")
        return redirect('post_list')
    post.delete()
    return redirect('post_list')

@login_required
def edit_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":

        post.title = request.POST.get('title')
        post.content = request.POST.get('content')

        # check if new image uploaded
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        post.save()

        return redirect('post_detail', post_id=post.id)

    return render(request, 'edit_post.html', {'post': post})

@login_required
def create_post(request):

    if request.method == "POST":

        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')

        Post.objects.create(
            title=title,
            content=content,
            image=image,
            author=request.user
        )

        return redirect('post_list')

    return render(request,'create_post.html')


def post_list(request):

    query = request.GET.get('q')

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        posts = Post.objects.all()

    return render(request, 'post_list.html', {'posts': posts})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            messages.error(request, "Invalid username or password")
            
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')
    return render(request, 'register.html')


def user_logout(request):
     logout(request)
     return redirect('login')


@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":

        content = request.POST.get('content')

        # Prevent empty comments
        if content.strip():

            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

    return redirect('post_detail', post_id=post.id)

def post_detail(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments
    })

@login_required
def like_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', post_id=post.id)

@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)

    # Only comment author can delete
    if comment.user == request.user:
        comment.delete()

    return redirect('post_detail', post_id=comment.post.id)