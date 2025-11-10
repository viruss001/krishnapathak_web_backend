from rest_framework import viewsets
from .models import ContactUs, Deletiondata
from .serializers import ContactUsSerializer, DeletiondataSerializer

class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

class DeletiondataViewSet(viewsets.ModelViewSet):
    queryset = Deletiondata.objects.all()
    serializer_class = DeletiondataSerializer
