from django.conf import settings
from django.views.generic.list import ListView

from .models import Post

BLOG_POSTS_PER_PAGE = getattr(settings, 'BLOG_POSTS_PER_PAGE', 10)
BLOG_POSTS_CONTEXT_NAME = getattr(
    settings, 'BLOG_POSTS_CONTEXT_NAME', 'object_list')


class PostListView(ListView):
    '''A view to display a list of blog posts'''

    paginate_by = BLOG_POSTS_PER_PAGE
    template = 'blog/post_list.html'
    context_object_name = BLOG_POSTS_CONTEXT_NAME

    def get_queryset(self):
        return Post.objects.filter(is_published=True)
