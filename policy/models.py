from django.db import models
from django.utils.text import slugify


class Policy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Heading(models.Model):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="headings")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    contains_only_bullet_points = models.BooleanField(default=False)

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return f"{self.policy.slug} — {self.title}"


class HeadingDescription(models.Model):
    heading = models.OneToOneField(Heading, on_delete=models.CASCADE, related_name="description")
    description = models.TextField(null=True, blank=True)
    contains_bullet_points = models.BooleanField(default=False)

    def __str__(self):
        return f"Description of {self.heading.title}"


class BulletPoint(models.Model):
    heading_description = models.ForeignKey(
        HeadingDescription, on_delete=models.CASCADE, related_name="bullet_points"
    )
    order = models.PositiveIntegerField(default=0)
    point = models.TextField()

    class Meta:
        ordering = ("order",)

    def __str__(self):
        snippet = (self.point[:50] + "...") if len(self.point) > 50 else self.point
        return f"• {snippet}"
