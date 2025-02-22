from django.shortcuts import render, get_object_or_404

from .models import BlogPost

def blog_list(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "blog/blog_detail.html", {"post": post})