from django.db import models
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from docutils.core import publish_parts
from jsonfield import JSONField

import markdown


class Attachment(models.Model):
    '''A model that contains information about an attachment in a blog post'''

    # A unique identifier that is used to embed within a blog post
    key = models.CharField(max_length=50)

    # Type of the attachment
    TYPE_IMAGE = 'IMAGE'
    TYPE_VIDEO = 'VIDEO'
    TYPE_AUDIO = 'AUDIO'
    TYPE_CHOICES = (
        (TYPE_IMAGE, 'Image'),
        (TYPE_VIDEO, 'Video'),
        (TYPE_AUDIO, 'Audio'),
    )
    type = models.CharField(
        max_length=16, choices=TYPE_CHOICES, default=TYPE_IMAGE)

    # Image attachment
    image = models.ImageField(
        upload_to='blog/attachment/', blank=True, null=True)

    # Youtube video attachment
    video = models.URLField(blank=True, null=True)

    # Soundcloud audio attachment
    audio = models.URLField(blank=True, null=True)

    # Used for extra html attributes for the embed code
    extra_properties = JSONField(default={})

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'

    def __str__(self):
        if self.type == self.TYPE_IMAGE:
            return self.image.url
        if self.type == self.TYPE_VIDEO:
            return self.video
        if self.type == self.TYPE_AUDIO:
            return self.audio

    def embed_code(self):
        '''Returns the embed code that can be used within the blog post'''
        attrs = []
        for key, value in self.extra_properties.items():
            attrs.append('%s="%s"' % (key, value))
        attrs_string = ' '.join(attrs)
        if self.type == self.TYPE_IMAGE:
            html = '<img src="%s" %s />' % (self.image.url, attrs_string)
        if self.type == self.TYPE_VIDEO:
            html = '<iframe src="%s" %s ></iframe>' % (
                self.video.url, attrs_string)
        if self.type == self.TYPE_AUDIO:
            html = '<iframe src="%s" %s ></iframe>' % (
                self.audio.url, attrs_string)
        return html


class Category(models.Model):
    '''A model that contains information about a blog post category'''

    # Name of the blog post category
    name = models.CharField(max_length=100)

    # Slug of the blog post category that will be used in URL
    slug = models.SlugField(max_length=100)

    # Parent of the category
    parent = models.ForeignKey('Category', blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def hierarchy(self):
        '''Returns the list of categories from the top most level to the
        current category'''
        hlist = [self]
        while hlist[0].parent:
            hlist = [hlist[0].parent] + hlist
        return hlist

    def get_absolute_url(self):
        '''Absolute URL of the blog posts by this category'''
        kwargs = {'category_slug': self.slug}
        return reverse('blog:posts_by_category', kwargs=kwargs)


class PostManager(models.Manager):
    '''A manager model for Post'''

    def published(self):
        '''Returns only published blog posts'''
        return self.get_queryset().filter(is_published=True)

    def category(self, category):
        '''Returns published blog posts of `category`'''
        queryset = self.published()
        categories = [category]
        index = 0
        while index < len(categories):
            current_category = categories[index]
            categories += list(Category.objects.filter(
                parent=current_category))
            index += 1
        return queryset.filter(categories__in=categories).distinct()


class Post(models.Model):
    '''A model that contains information about a blog post'''

    # Title of the blog post
    title = models.CharField(max_length=100)

    # Slug of the blog post which is used in the URL
    slug = models.SlugField(max_length=100)

    # An optional tag line for the blog post
    tag_line = models.CharField(max_length=100, blank=True, null=True)

    # Type of the blog post
    TYPE_STANDARD = 'STANDARD'
    TYPE_IMAGE = 'IMAGE'
    TYPE_VIDEO = 'VIDEO'
    TYPE_AUDIO = 'AUDIO'
    TYPE_CHOICES = (
        (TYPE_STANDARD, 'Standard'),
        (TYPE_IMAGE, 'Image'),
        (TYPE_VIDEO, 'Video'),
        (TYPE_AUDIO, 'Audio'),
    )
    type = models.CharField(
        max_length=16, choices=TYPE_CHOICES, default=TYPE_STANDARD)

    # Markup language used in content and summary
    MARKUP_LANGUAGE_HTML = 'HTML'
    MARKUP_LANGUAGE_MARKDOWN = 'MD'
    MARKUP_LANGUAGE_RST = 'RST'
    MARKUP_LANGUAGE_CHOICES = (
        (MARKUP_LANGUAGE_HTML, 'HTML'),
        (MARKUP_LANGUAGE_MARKDOWN, 'Markdown'),
        (MARKUP_LANGUAGE_RST, 'reStructuredText')
    )
    markup_language = models.CharField(
        max_length=50, choices=MARKUP_LANGUAGE_CHOICES,
        default=MARKUP_LANGUAGE_HTML)

    # Content of the blog post
    content = models.TextField()

    # Summary of the blog post
    summary = models.TextField()

    # Categories of the blog post
    categories = models.ManyToManyField(Category)

    # Only published fields are visible on the site
    is_published = models.BooleanField(default=False)

    # Date to be displayed on the blog post
    published_on = models.DateTimeField(blank=True, null=True, db_index=True)

    # Optional featured blog post
    is_featured = models.BooleanField(default=False)

    # Created and updated datetime of the blog post
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # Featured image is shown in blog teaser if the type is Image
    featured_image = models.ImageField(
        upload_to='blog/post/', blank=True, null=True)

    # Featured youtube video is shown in blog teaser if the type is Video
    featured_video = models.URLField(blank=True, null=True)

    # Featured soundcloud audio is shown in blog teaser if the type is Audio
    featured_audio = models.URLField(blank=True, null=True)

    # Attachments included in the blog post
    attachments = models.ManyToManyField(Attachment, blank=True)

    # Manager model
    objects = PostManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-published_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        '''Absolute URL of the blog post'''
        kwargs = {
            'year': str(self.published_on.year),
            'month': '%02d' % self.published_on.month,
            'slug': self.slug
        }
        return reverse('blog:post', kwargs=kwargs)

    def get_attachments(self):
        '''Returns a dictionary of attachment key and attachment embed code'''
        attachments = {}
        for attachment in self.attachments.all():
            attachments[attachment.key] = attachment.embed_code()
        return attachments

    def content_html(self):
        '''Returns the content as HTML based on the markup language used'''
        if self.markup_language == self.MARKUP_LANGUAGE_HTML:
            html = self.content
        if self.markup_language == self.MARKUP_LANGUAGE_MARKDOWN:
            html = markdown.markdown(self.content)
        if self.markup_language == self.MARKUP_LANGUAGE_RST:
            html = publish_parts(self.content, writer_name='html')['html_body']
        attachments = self.get_attachments()
        html = html.format(**attachments)
        return mark_safe(html)

    def summary_html(self):
        '''Returns the summary as HTML based on the markup language used'''
        if self.markup_language == self.MARKUP_LANGUAGE_HTML:
            html = self.summary
        if self.markup_language == self.MARKUP_LANGUAGE_MARKDOWN:
            html = markdown.markdown(self.summary)
        if self.markup_language == self.MARKUP_LANGUAGE_RST:
            html = publish_parts(self.summary, writer_name='html')['html_body']
        attachments = self.get_attachments()
        html = html.format(**attachments)
        return mark_safe(html)
