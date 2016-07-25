# django-minimal-blog
A minimalistic blog app for django
## Quickstart
Add blog to INSTALLED_APPS in settings.py of your project
```
INSTALLED_APPS = [
    ...
    'blog',
]
```
Add blog urls to urlpatterns in urls.py of your project
```
urlpatterns = [
    ...
    url(r'^blog/', include('blog.urls', namespace='blog')),
]
```

## URLs

1. `/blog/`: URL to display the list of paginated blog posts.
2. `/blog/{category}/`: URL to display the list of paginated blog posts of a particular category.
3. `/blog/post/{year}/{month}/{slug}/`: URL to display a blog post.

Provide the following templates:

1. `blog/post_list.html`: Template to display the list of blog post. Context variables: `posts`, `category`
2. `blog/post.html`: Template to display a blog post. Context variable: `post`

## Templatetags
Loading templatetags: `{% load blog_extras %}`

1. `recent_posts`:  Returns a list of recent blog posts.
2. `featured_posts`: Returns a list of blog posts marked as featured.

Example:
```
{% load blog_extras %}

{% recent_posts as posts %}
{% for post in posts %}
    {{ post.title }}
{% endfor %}
```

## Settings

1. `BLOG_POSTS_PER_PAGE`: Number of posts per page. Default: `10`
2. `BLOG_POST_LIST_CONTEXT_NAME`: Context variable name used in `blog/post_list.html` template. Default: `posts`
3. `BLOG_POST_CONTEXT_NAME`: Context varaible name used in `blog/post.html` template. Default: `post`
