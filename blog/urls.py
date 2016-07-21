from django.conf import settings
from django.conf.urls import url

from . import views

# Making blog URLs flexible by updating the default URLs with custom URLS
# Using this updated dictionary for generating URLs
BLOG_URLS = {
    'post_list': r'^posts/$',
    'post': r'^(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w-]+)/$',
}
BLOG_URLS.update(getattr(settings, 'BLOG_URLS', {}))


urlpatterns = [
    # URL to display the list of paginated blog posts
    url(BLOG_URLS['post_list'], views.PostListView.as_view(),
        name='post_list'),

    # URL to display a blog post
    url(BLOG_URLS['post'], views.PostView.as_view(), name='post'),
]
