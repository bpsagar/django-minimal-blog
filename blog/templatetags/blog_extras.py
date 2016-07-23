from django import template
from django.apps import apps

register = template.Library()


@register.simple_tag
def recent_posts():
    Post = apps.get_model('blog', 'Post')
    return Post.objects.published()


@register.simple_tag
def featured_posts():
    Post = apps.get_model('blog', 'Post')
    return Post.objects.published().filter(is_featured=True)
