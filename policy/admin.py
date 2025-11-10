from django.contrib import admin
from .models import Policy, Heading, HeadingDescription, BulletPoint


class BulletPointInline(admin.TabularInline):
    model = BulletPoint
    extra = 0
    fields = ("order", "point")


class HeadingDescriptionInline(admin.StackedInline):
    model = HeadingDescription
    extra = 0
    readonly_fields = ("contains_bullet_points",)
    inlines = [BulletPointInline]  # ✅ NEST bullet points here


@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    inlines = [HeadingDescriptionInline]
    list_display = ("title", "policy", "order", "contains_only_bullet_points")
    list_filter = ("policy",)


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(BulletPoint)
class BulletPointAdmin(admin.ModelAdmin):
    list_display = ("point", "heading_description", "order")
