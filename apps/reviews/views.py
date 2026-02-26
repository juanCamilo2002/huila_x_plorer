from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        spot_id = self.request.query_params.get('post')
        qs = Review.objects.all()

        if spot_id:
            qs = qs.filter(tourist_spot_id=spot_id)
        
        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAuthenticated()]