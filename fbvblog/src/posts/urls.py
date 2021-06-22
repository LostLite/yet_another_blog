from django.urls import path

from .views import (
    index, blog,
    post, search,
    post_create, post_delete, post_update
)

urlpatterns = [
    path('', index, name='home'),
    path('blog/', blog, name='blog'),
    path('search/', search, name='search'),
    path('create/', post_create, name='post-create'),
    path('post/<int:id>/', post, name='post'),
    path('post/<int:id>/update/', post_update, name='post-update'),
    path('post/<int:id>/delete/', post_delete, name='post-delete'),
]
