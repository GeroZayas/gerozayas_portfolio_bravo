from django.db import models
from django.template.defaultfilters import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
        indexes = [
            models.Index(fields=['name']),
        ]

    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        ordering = ['-created_on']
        indexes = [
            models.Index(fields=['is_active', '-created_on']),
            models.Index(fields=['slug']),
        ]

    name = models.CharField(max_length=255)
    body = MarkdownxField(blank=True, null=True)
    body_html = models.TextField(blank=True, editable=False)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True, db_index=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    image = models.ImageField(upload_to="blog/covers/", blank=True, help_text="Upload blog post cover image")
    is_active = models.BooleanField(default=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Convert markdown to HTML and cache
        if self.body:
            self.body_html = markdownify(self.body)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/blog/{self.slug}/"


class Comment(models.Model):
    class Meta:
        ordering = ['-created_on']
        indexes = [
            models.Index(fields=['post', '-created_on']),
        ]

    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.author} on {self.post.name}"


# Cache invalidation signals
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver


@receiver([post_save, post_delete], sender=Post)
def clear_post_cache(sender, instance, **kwargs):
    """Clear relevant caches when post is modified."""
    try:
        cache.delete(f'post_{instance.pk}')
        # Clear all blog page caches
        from django_redis import get_redis_connection
        con = get_redis_connection("default")
        con.delete_pattern("*blog*")
    except Exception as e:
        # If Redis is not available, fail silently
        pass


@receiver(m2m_changed, sender=Post.categories.through)
def clear_category_cache(sender, instance, **kwargs):
    """Clear cache when post categories change."""
    try:
        cache.delete(f'post_{instance.pk}')
        from django_redis import get_redis_connection
        con = get_redis_connection("default")
        con.delete_pattern("*blog*")
    except Exception as e:
        pass
