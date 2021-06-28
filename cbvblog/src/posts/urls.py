from django.urls import path

from .views import (
    IndexView, BlogListView,
    PostDetailView, SearchView,
    PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('search/', SearchView.as_view(), name='search'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
