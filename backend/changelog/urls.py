from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChangelogViewSet

router = DefaultRouter()
router.register(r'changelog', ChangelogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
