from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from .models import Post


class PostListView(ListView):
    '''A view to display a list of blog posts'''

    paginate_by = getattr(settings, 'BLOG_POSTS_PER_PAGE', 10)
    context_object_name = getattr(
        settings, 'BLOG_POST_LIST_CONTEXT_NAME', 'posts')
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostView(TemplateView):
    '''A view to display a blog post'''

    context_object_name = getattr(settings, 'BLOG_POST_CONTEXT_NAME', 'post')
    template_name = 'blog/post.html'

    def get_context_data(self, **kwargs):
        context = {}
        context[self.context_object_name] = Post.objects.get(
            slug=kwargs.get('slug'))
        return context

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs.get('slug'))

        if 'year' in kwargs:
            if post.published_on.year != int(kwargs.get('year')):
                raise Http404

        if 'month' in kwargs:
            if post.published_on.month != int(kwargs.get('month')):
                raise Http404
        return super(PostView, self).dispatch(request, *args, **kwargs)
