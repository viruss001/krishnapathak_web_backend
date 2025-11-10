from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PriceSection, BulletPoints
from .serializers import PriceSectionSerializer, BulletPointsSerializer
from django.shortcuts import get_object_or_404


# -----------------------------
# PRICE SECTION VIEWS
# -----------------------------
class PriceSectionList(APIView):
    """Handles GET (list all) and POST (create new) for PriceSection"""

    def get(self, request):
        prices = PriceSection.objects.all()
        serializer = PriceSectionSerializer(prices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PriceSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriceSectionDetail(APIView):
    """Handles GET, PUT, DELETE for a single PriceSection"""

    def get_object(self, pk):
        return get_object_or_404(PriceSection, pk=pk)

    def get(self, request, pk):
        price_section = self.get_object(pk)
        serializer = PriceSectionSerializer(price_section)
        return Response(serializer.data)

    def put(self, request, pk):
        price_section = self.get_object(pk)
        serializer = PriceSectionSerializer(price_section, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        price_section = self.get_object(pk)
        price_section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------------
# BULLET POINT VIEWS
# -----------------------------
class BulletPointsList(APIView):
    """Handles GET (list all or by price_id) and POST (create new) for BulletPoints"""

    def get(self, request):
        price_id = request.query_params.get('price_id')  # ?price_id=1
        if price_id:
            bullets = BulletPoints.objects.filter(title_id=price_id)
        else:
            bullets = BulletPoints.objects.all()

        serializer = BulletPointsSerializer(bullets, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Expected JSON:
        {
            "price_id": 3,
            "points": "Unlimited internet access"
        }
        """
        price_id = request.data.get("price_id")

        if not price_id:
            return Response(
                {"error": "Missing 'price_id' in request body"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the related PriceSection
        price_section = get_object_or_404(PriceSection, id=price_id)

        # Create the bullet point and link it
        bullet = BulletPoints.objects.create(
            title=price_section,
            points=request.data.get("points", "")
        )

        serializer = BulletPointsSerializer(bullet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BulletPointsDetail(APIView):
    """Handles GET, PUT, DELETE for a single BulletPoint"""

    def get_object(self, pk):
        return get_object_or_404(BulletPoints, pk=pk)

    def get(self, request, pk):
        bullet = self.get_object(pk)
        serializer = BulletPointsSerializer(bullet)
        return Response(serializer.data)

    def put(self, request, pk):
        bullet = self.get_object(pk)
        serializer = BulletPointsSerializer(bullet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bullet = self.get_object(pk)
        bullet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
