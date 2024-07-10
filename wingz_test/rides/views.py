from rest_framework import viewsets, mixins, status
from rest_framework.pagination import PageNumberPagination
from .models import Ride, User, RideEvent
from .serializers import RideSerializer, UserSerializer, RideEventSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RidePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 20


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    pagination_class = RidePagination

    def get_queryset(self):
        queryset = Ride.objects.all()
        status = self.request.query_params.get("status", None)
        email = self.request.query_params.get("email", None)
        sort = self.request.query_params.get("sort", None)
        order = "" if self.request.query_params.get("ascending") == "true" else "-"
        if status:
            queryset = queryset.filter(status=status)
        if email:
            queryset = queryset.filter(rider__email=email)
        if sort:
            sort = order + sort
            queryset = queryset.order_by(sort)
        return queryset


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
