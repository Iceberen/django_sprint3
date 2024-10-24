from datetime import datetime

from django.shortcuts import render, get_object_or_404

from .models import Post, Category
from .constants import QUANTITY_ON_INDEX


def index(request):
    template = 'blog/index.html'
    posts_list = Post.objects.select_related('category').filter(
        is_published=True,
        category__is_published=True,
        pub_date__date__lt=datetime.now()).order_by(
            'pub_date')[:QUANTITY_ON_INDEX]
    context = {'post_list': posts_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.select_related('category'),
        pub_date__date__lt=datetime.now(),
        category__is_published=True,
        is_published=True,
        pk=post_id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts_list = category.posts.filter(
        category__slug=category_slug,
        is_published=True,
        category__is_published=True,
        pub_date__date__lt=datetime.now()
    )
    context = {'category': category, 'post_list': posts_list}
    return render(request, template, context)
