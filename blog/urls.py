from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^blog/posts/$', views.PostListView.as_view(), name='post_list'),
]
