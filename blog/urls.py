from django.conf import settings
from django.conf.urls import url

from . import views

# Making blog URLs flexible by updating the default URLs with custom URLS
# Using this updated dictionary for generating URLs
BLOG_URLS = {
    'post_list': r'^posts/$',
    'posts_by_category': r'^posts/(?P<category>[\w]+)/$',
    'post': r'post/^(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w-]+)/$',
}
BLOG_URLS.update(getattr(settings, 'BLOG_URLS', {}))


urlpatterns = [
    # URL to display the list of paginated blog posts
    url(BLOG_URLS['post_list'], views.PostListView.as_view(),
        name='post_list'),

    # URL to display the list of paginated blog posts of a particular category
    url(BLOG_URLS['posts_by_category'], views.PostsByCategoryView.as_view(),
        name='posts_by_category'),

    # URL to display a blog post
    url(BLOG_URLS['post'], views.PostView.as_view(), name='post'),
]
