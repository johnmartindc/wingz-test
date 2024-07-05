from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rides import views

router = DefaultRouter()
router.register(r"rides", views.RideViewSet, basename="Ride")
router.register(r"users", views.UserViewSet)
router.register(r"ride_event", views.RideEventViewSet)

urlpatterns = [path("admin/", admin.site.urls), path("", include(router.urls))]
