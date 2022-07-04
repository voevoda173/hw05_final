from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from .utils import pagin


def index(request):
    """
    Метод, предназначенный для вывода данных при
    обращении к главной странице сайта.
    """
    posts = Post.objects.select_related(
        'author',
        'group',
    )
    page_obj = pagin(request, posts)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """
    Метод, предназначенный для вывода данных при
    обращении к публикациям в тематической группе.
    """
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related(
        'author',
        'group',
    )
    page_obj = pagin(request, posts)
    context = {
        'group': group,
        'page_obj': page_obj,
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """
    Метод, предназначенный для данных
    обо всех записях пользователя.
    """
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related(
        'author',
        'group',
    )
    page_obj = pagin(request, posts)
    following = request.user.is_authenticated and (
        Follow.objects.filter(
            user=request.user,
            author=author,
        ).exists()
    )
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following,
    }

    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Метод, предназначенный для представления данных
    о деталях записи.
    """
    post = get_object_or_404(Post.objects.select_related(
        'author',
        'group',
    ), id=post_id)
    form = CommentForm(request.POST or None)
    comments = post.comments.select_related(
        'post',
    )
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }

    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Метод, предназначенный создания новой записи."""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()

            return redirect('posts:profile', username=post.author)
    context = {
        'form': form,
    }

    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    """Метод, предназначенный редактирования новой записи."""
    post = get_object_or_404(Post.objects.select_related(
        'author',
        'group',
    ), id=post_id)

    if request.user != post.author:

        return redirect('posts:post_detail', post.pk)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    if not form.is_valid():

        return render(request, 'posts/create_post.html', context)

    form.save()

    return redirect('posts:post_detail', post.pk)


@login_required
def add_comment(request, post_id):
    """Метод, предназначенный для комментирования записей."""
    post = get_object_or_404(Post.objects.select_related(
        'author',
        'group',
    ), id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Метод, предназаначенный для получения постов автора,
    на которого подписан текущий пользователь."""
    posts = Post.objects.select_related(
        'author',
        'group',
    ).filter(author__following__user=request.user)
    page_obj = pagin(request, posts)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author == request.user or Follow.objects.filter(
            user=request.user, author=author).exists():

        return redirect('posts:profile', username)

    Follow.objects.create(user=request.user, author=author)

    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()

    return redirect('posts:profile', username)
