from django.urls import path
from . import views

urlpatterns = [
    path("", views.PolicyListCreateAPIView.as_view(), name="policy-list-create"),
    path("<slug:slug>/", views.PolicyRetrieveUpdateDestroyAPIView.as_view(), name="policy-detail"),
]
