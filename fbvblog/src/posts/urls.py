from django.urls import path

from .views import index, blog, post, search

urlpatterns = [
    path('', index, name='home'),
    path('blog/', blog, name='blog'),
    path('search/', search, name='search'),
    path('post/<int:id>/', post, name='post'),
]
