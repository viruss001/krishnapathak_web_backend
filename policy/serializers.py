# serializers.py
from rest_framework import serializers
from .models import Policy, Heading, HeadingDescription, BulletPoint


class BulletPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletPoint
        fields = ("id", "order", "point")


class HeadingDescriptionSerializer(serializers.ModelSerializer):
    bullet_points = BulletPointSerializer(many=True, required=False)

    class Meta:
        model = HeadingDescription
        fields = ("id", "description", "contains_bullet_points", "bullet_points")

    def create(self, validated_data):
        bullets = validated_data.pop("bullet_points", [])
        hd = HeadingDescription.objects.create(**validated_data)
        for bp in bullets:
            BulletPoint.objects.create(heading_description=hd, **bp)
        return hd


class HeadingSerializer(serializers.ModelSerializer):
    description = HeadingDescriptionSerializer(required=False)

    class Meta:
        model = Heading
        fields = ("id", "title", "order", "contains_only_bullet_points", "description")

    def create(self, validated_data):
        desc_data = validated_data.pop("description", None)
        heading = Heading.objects.create(**validated_data)
        if desc_data:
            HeadingDescription.objects.create(heading=heading, **desc_data)
        return heading


class PolicySerializer(serializers.ModelSerializer):
    headings = HeadingSerializer(many=True, required=False)

    class Meta:
        model = Policy
        fields = ("id", "title", "slug", "description", "headings")

    def create(self, validated_data):
        headings_data = validated_data.pop("headings", [])
        policy = Policy.objects.create(**validated_data)
        for hd_data in headings_data:
            HeadingSerializer().create({**hd_data, "policy": policy})
        return policy
