from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

# Create your models here.
class Project(models.Model):
    class Meta:
        verbose_name_plural = "Portfolio Profiles"
        verbose_name = "Portfolio"
        ordering = ["ranking"]

    title = models.CharField(max_length=100)
    description = models.TextField()
    body = RichTextField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, max_length=255)
    is_active = models.BooleanField(default=True)
    technology = models.CharField(max_length=40)
    github_link = models.URLField(max_length=200)
    image = models.ImageField(upload_to="static/images/Projects/")

    ranking = models.IntegerField(default=7)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/portfolio/{self.slug}"
