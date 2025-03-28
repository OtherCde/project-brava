from django.shortcuts import render
from rest_framework import generics
from .models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework.permissions import AllowAny

# Create your views here.
class AdvertisementListView(generics.ListAPIView):
    serializer_class = AdvertisementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Retorna solo las publicidades activas."""
        return Advertisement.objects.filter(status='active')