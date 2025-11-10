from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BulletPoint


@receiver([post_save, post_delete], sender=BulletPoint)
def update_contains_bullet_points(sender, instance, **kwargs):
    """
    Keep HeadingDescription.contains_bullet_points and Heading.contains_only_bullet_points
    logically correct:

    - contains_bullet_points = True if there are any bullets.
    - contains_only_bullet_points = True if there are bullets but NO text description.
    """

    hd = instance.heading_description
    heading = hd.heading

    has_bullets = hd.bullet_points.exists()
    has_description = bool(hd.description and hd.description.strip())

    # Update HeadingDescription.contains_bullet_points
    if hd.contains_bullet_points != has_bullets:
        hd.contains_bullet_points = has_bullets
        hd.save(update_fields=["contains_bullet_points"])

    # Update Heading.contains_only_bullet_points
    only_bullets = has_bullets and not has_description
    if heading.contains_only_bullet_points != only_bullets:
        heading.contains_only_bullet_points = only_bullets
        heading.save(update_fields=["contains_only_bullet_points"])
