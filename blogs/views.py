from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Blog, Comment, Notification
from .forms import BlogForm, CommentForm
from django.core.paginator import Paginator
from django.db.models import Q

def blog_list(request):
    query = request.GET.get('q')
    blogs = Blog.objects.all().order_by('-created_at')
    if query:
        blogs = blogs.filter(Q(title__icontains=query))
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs/blog_list.html', {'page_obj': page_obj, 'query': query})

@login_required
def my_blogs(request):
    blogs = Blog.objects.filter(author=request.user).order_by('-created_at')
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs/my_blogs.html', {'page_obj': page_obj})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blogs:blog_list')
    else:
        form = BlogForm()
    return render(request, 'blogs/create_blog.html', {'form': form})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comments.filter(parent__isnull=True)
    paginator = Paginator(comments, 3)
    page_number = request.GET.get('comment_page')
    comment_page_obj = paginator.get_page(page_number)
    comment_form = CommentForm()
    return render(request, 'blogs/blog_detail.html', {
        'blog': blog,
        'comment_page_obj': comment_page_obj,
        'comment_form': comment_form,
    })

@login_required
def update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.author != request.user:
        return HttpResponseForbidden("You cannot edit this blog")
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog_detail', pk=pk)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blogs/update_blog.html', {'form': form, 'blog': blog})

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You cannot delete this blog")
    if request.method == 'POST':
        blog.delete()
        return redirect('blogs:blog_list')
    return render(request, 'blogs/delete_blog.html', {'blog': blog})

@login_required
def like_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.author != request.user:
        if request.user in blog.likes.all():
            blog.likes.remove(request.user)
        else:
            blog.likes.add(request.user)
            Notification.objects.create(
                recipient=blog.author,
                actor=request.user,
                verb="liked",
                target_type="blog",
                target_id=blog.id
            )
    return redirect('blogs:blog_detail', pk=pk)

@login_required
def add_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            if blog.author != request.user:
                Notification.objects.create(
                    recipient=blog.author,
                    actor=request.user,
                    verb="commented",
                    target_type="blog",
                    target_id=blog.id
                )
            return redirect('blogs:blog_detail', pk=pk)
    return redirect('blogs:blog_detail', pk=pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You cannot edit this comment.")
    blog_id = comment.blog.id
    comment.delete()
    return redirect('blogs:blog_detail', pk=blog_id)


@login_required
def update_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden("You cannot edit this comment.")
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog_detail', pk=comment.blog.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blogs/update_comment.html', {'form': form, 'comment': comment})

@login_required
def add_reply(request, pk, comment_id):
    blog = get_object_or_404(Blog, pk=pk)
    parent_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.blog = blog
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
            if parent_comment.author != request.user:
                Notification.objects.create(
                    recipient=parent_comment.author,
                    actor=request.user,
                    verb="replied to your comment to",
                    target_type="blog",
                    target_id=blog.id
                )
            return redirect('blogs:blog_detail', pk=pk)
    return redirect('blogs:blog_detail', pk=pk)