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
    url(r'^blog/', include('blog.urls')),
]
```
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
4. `BLOG_URLS`: Dictionary to specify custom URLs
  1. `post_list`: URL for blog post list view.
  2. `posts_by_category`: URL for blog posts by category. Requires `category` in URL.
  3. `post`: URL for blog post view. Requires `slug` and an optional `year` and `month` in URL.
