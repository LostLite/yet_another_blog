from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from .models import Post, Author, PostView
from .forms import CommentForm, PostForm
from marketing.models import Signup


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:  # search query has been submitted
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(overview__icontains=query)
            ).distinct()

        context = {
            'queryset': queryset
        }

        return render(request, 'search_results.html', context)


def get_category_count():
    # annotate returns a dictionary where each key is going to be each category
    queryset = Post.objects.values(
        'categories__title').annotate(Count('categories__title'))

    return queryset


class IndexView(View):
    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]

        context = {
            'object_list': featured,
            'latest': latest
        }
        return render(request, template_name="index.html", context=context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

        messages.info(request, "Successfully subscribed")

        return redirect('home')


class BlogListView(ListView):
    model = Post
    template_name = 'blog.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]

        context['most_recent'] = most_recent
        context['category_count'] = category_count
        context['page_request_var'] = "page"

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    # This method is always called whenever this view is called
    def get_object(self):
        obj = super().get_object()

        # increase counter for object being viewed
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]

        context['most_recent'] = most_recent
        context['category_count'] = category_count
        context['form'] = self.form

        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = self.get_object()
            form.save()
            return redirect(reverse('post', kwargs={
                'pk': form.instance.post.id,
            }))


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse('post', kwargs={
            'pk': form.instance.id,
        }))


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse('post', kwargs={
            'pk': form.instance.id,
        }))


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/blog'
