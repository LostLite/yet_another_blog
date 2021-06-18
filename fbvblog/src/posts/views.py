from django.shortcuts import render
from .models import Post
from marketing.models import Signup


def index(request):

    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest
    }
    return render(request, template_name="index.html", context=context)


def blog(request):
    return render(request, template_name='blog.html', context={})


def post(request):
    return render(request, template_name='post.html', context={})
