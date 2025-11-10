from rest_framework import generics
from .models import Policy
from .serializers import PolicySerializer

class PolicyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class PolicyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    lookup_field = "slug"
