from django.db import models


class ContactProfile(models.Model):
    class Meta:
        verbose_name_plural = "Contact Profiles"
        verbose_name = "Contact Profile"
        ordering = ["timestamp"]
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    name = models.CharField(verbose_name="Name", max_length=100)
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Message")

    def __str__(self):
        return f"{self.name}"


class Certificate(models.Model):
    class Meta:
        verbose_name_plural = "Certificates"
        verbose_name = "Certificate"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=['is_active', '-date']),
        ]

    date = models.DateTimeField(blank=True, null=True, db_index=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    certificate_link = models.URLField(
        max_length=200, default="www.github.com/gerozayas"
    )
    certificate_image = models.ImageField(upload_to="certificates/")

    def __str__(self):
        return self.name
