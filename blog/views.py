import os
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from config.settings import MEDIA_ROOT
from .forms import PostForm, CommentForm, ImageForm
from .models import Post, Image
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def blog(request):
    post_list = Post.objects.order_by('-create_date')
    context = {'post_list': post_list}
    return render(request, 'blog/blog_home.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    images = Image.objects.filter(post=post)
    context = {'post': post, 'images': images}
    return render(request, 'blog/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        image_form = ImageForm(request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # author 속성에 로그인 계정 저장
            post.create_date = timezone.now()
            post.save()

            for img in files:
                Image.objects.create(post=post, image=img)

            return redirect('blog:blog')
    else:
        form = PostForm()
        image_form = ImageForm()
    context = {'form': form, 'image_form': image_form}
    return render(request, 'blog/post_create.html', context)


def post_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    image_form = ImageForm(request.FILES)
    files = request.FILES.getlist('image')
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modify_date = timezone.now()  # 수정일시 저장
            post.save()
            images = Image.objects.filter(post=post)
            for img in images:
                os.remove(os.path.join(MEDIA_ROOT, img.image.name))
                img.delete()
            for img in files:
                Image.objects.create(post=post, image=img)

            return redirect('blog:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
        image_form = ImageForm()
    context = {'form': form, 'image_form': image_form}
    return render(request, 'blog/post_create.html', context)


def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('blog:post_detail', post_id=post.id)
    images = Image.objects.filter(post=post)
    for img in images:
        os.remove(os.path.join(MEDIA_ROOT, img.image.name))
        img.delete()
    post.delete()
    return redirect('blog:blog')


def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # author 속성에 로그인 계정 저장
            comment.create_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('blog:post_detail', post_id=post.id), comment.id))
    else:
        form = CommentForm()
    context = {'post': post, 'form': form}
    return render(request, 'blog/post_detail.html', context)



