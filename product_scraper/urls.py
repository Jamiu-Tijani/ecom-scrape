from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ScraperViewSet


router = DefaultRouter()
router.register(
    r"scraper",
    ScraperViewSet,
    basename="scraper",
)
router.register(r"", ScraperViewSet, basename="scraper")


urlpatterns = [
    path("", include(router.urls)),
]
