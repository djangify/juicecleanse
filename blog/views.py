from django.shortcuts import render,get_object_or_404
from .models import BlogPost

def blog_list(request):
    featured=BlogPost.objects.filter(is_featured=True).order_by('-created_at')[:5]
    posts=BlogPost.objects.all().order_by('-created_at')
    return render(request,'blog/blog_list.html',{'featured_posts':featured,'all_posts':posts})

def blog_detail(request,slug):
    post=get_object_or_404(BlogPost,slug=slug)
    return render(request,'blog/blog_detail.html',{'post':post})