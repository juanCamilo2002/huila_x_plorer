from rest_framework.routers import DefaultRouter
from .views import TouristSoptImageViewSet, TouristSpotViewsSet

router = DefaultRouter()
router.register(r'spots', TouristSpotViewsSet, basename='spots')
router.register(r'spot-images', TouristSoptImageViewSet, basename='spot-images')

urlpatterns = router.urls
