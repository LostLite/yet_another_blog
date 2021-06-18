from django.urls import path

from .views import index, blog, post

urlpatterns = [
    path('', index, name='home'),
    path('blog/', blog, name='blog'),
    path('post/', post, name='post'),
]
