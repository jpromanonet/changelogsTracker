from rest_framework import viewsets
from .models import Changelog
from .serializers import ChangelogSerializer

class ChangelogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Changelog.objects.all()
    serializer_class = ChangelogSerializer
