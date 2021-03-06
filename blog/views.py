from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm
from .models import Comment, Post


def post_list(request):
    """ Returns a list of posts and the number of unapproved comments."""
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    unapproved_comments = Comment.objects.filter(approved_comment=False).count
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'unapproved_comments': unapproved_comments
        })

@login_required
def unapproved_comments(request):
    unapproved_comments = Comment.objects.filter(approved_comment=False)
    return render(request, 'blog/unapproved_comments.html', {
        'unapproved_comment_list': unapproved_comments
        })


def post_detail(request, pk):
    """ Returns a post and the number of unapproved comments."""
    post = get_object_or_404(Post, pk=pk)
    unapproved_comments = Comment.objects.filter(approved_comment=False).count
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'unapproved_comments': unapproved_comments
        })


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog.views.post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)


def about_site(request):
    return render(request, 'blog/about_site.html')


def site_links(request):
    return render(request, 'blog/site_links.html')

