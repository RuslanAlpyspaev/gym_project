from rest_framework import viewsets
from .models import Environment
from .serializers import EnvironmentSerializer


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
