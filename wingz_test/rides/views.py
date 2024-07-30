from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
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

    @action(detail=False, methods=["get"])
    def sort_by_distance(self, request):
        from django.db.models import Case, When, IntegerField

        latitude = request.query_params.get("latitude", None)
        longitude = request.query_params.get("longitude", None)
        reverse = (
            True if self.request.query_params.get("ascending") == "false" else False
        )

        if latitude is None or longitude is None:
            return Response(
                {"error": "Please provide latitude and longitude."}, status=400
            )

        queryset = self.get_queryset()

        rides_with_distance = [
            (ride, ride.distance_to_pickup(latitude, longitude)) for ride in queryset
        ]
        rides_with_distance.sort(key=lambda x: x[1], reverse=reverse)

        pk_list = [ride.pk for ride, distance in rides_with_distance]
        queryset = queryset.annotate(
            custom_order=Case(
                *[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)],
                output_field=IntegerField(),
            )
        ).order_by("custom_order")
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=200)


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
