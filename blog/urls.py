from django.conf import settings
from django.conf.urls import url

from . import views

# Making blog URLs flexible by updating the default URLs with custom URLS
# Using this updated dictionary for generating URLs
BLOG_URLS = {
    'post_list': r'^posts/$',
}
BLOG_URLS.update(getattr(settings, 'BLOG_URLS', {}))


urlpatterns = [
    # URL to display the list of paginated blog posts
    url(BLOG_URLS['post_list'], views.PostListView.as_view(),
        name='post_list'),
]
