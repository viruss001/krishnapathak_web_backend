from rest_framework import serializers
from .models import ContactUs ,Deletiondata

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
class DeletiondataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deletiondata
        fields = '__all__'
