from django.urls import path
from .views import (
    PriceSectionList, PriceSectionDetail,
    BulletPointsList, BulletPointsDetail
)

urlpatterns = [
    path('prices/', PriceSectionList.as_view(), name='price-list'),
    path('prices/<int:pk>/', PriceSectionDetail.as_view(), name='price-detail'),

    path('bullets/', BulletPointsList.as_view(), name='bullet-list'),
    path('bullets/<int:pk>/', BulletPointsDetail.as_view(), name='bullet-detail'),
]
