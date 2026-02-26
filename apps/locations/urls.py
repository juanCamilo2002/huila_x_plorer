from rest_framework.routers import DefaultRouter
from .views import TouristSoptImageViewSet, TouristSpotViewsSet, FavoriteViewSet

router = DefaultRouter()
router.register(r'spots', TouristSpotViewsSet, basename='spots')
router.register(r'spot-images', TouristSoptImageViewSet, basename='spot-images')
router.register(r'favorites', FavoriteViewSet, basename='favorites')

urlpatterns = router.urls
