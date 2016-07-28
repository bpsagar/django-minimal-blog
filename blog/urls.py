from django.conf.urls import url

from . import views


urlpatterns = [
    # URL to display the list of paginated blog posts
    url(r'^$', views.PostListView.as_view(), name='post_list'),

    # URL to display the list of paginated blog posts of a particular category
    url(r'^(?P<category_slug>[\w-]+)/$', views.PostsByCategoryView.as_view(),
        name='posts_by_category'),

    # URL to display a blog post
    url(r'^post/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w-]+)/$',
        views.PostView.as_view(), name='post'),
]
