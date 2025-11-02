from django.db import models
from django.template.defaultfilters import slugify


class Project(models.Model):
    class Meta:
        verbose_name_plural = "Portfolio Projects"
        verbose_name = "Project"
        ordering = ["ranking"]
        indexes = [
            models.Index(fields=['is_active', 'ranking']),
            models.Index(fields=['slug']),
        ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    body = models.TextField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    technology = models.CharField(max_length=40)
    github_link = models.URLField(max_length=200)
    image = models.ImageField(upload_to="projects/")
    ranking = models.IntegerField(default=7, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/portfolio/{self.slug}/"
