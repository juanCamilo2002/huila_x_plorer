from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, RouteStopViewSet

router = DefaultRouter()
router.register(r'', RouteViewSet, basename='routes')
router.register(r'stops', RouteStopViewSet, basename='route-stops')

urlpatterns = router.urls
