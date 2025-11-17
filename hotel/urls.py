from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomViewSet, BookingViewSet, OfflineBookingViewSet, BookingRequestViewSet,
    UserProfileViewSet, TestimonialViewSet, VideoItemViewSet,login_view, MediaItemViewSet
)
from .views import send_enquiry

router = DefaultRouter()
router.register("rooms", RoomViewSet)
router.register("bookings", BookingViewSet)
router.register("offline-bookings", OfflineBookingViewSet)
router.register("booking-requests", BookingRequestViewSet)
router.register("users", UserProfileViewSet)
router.register("testimonials", TestimonialViewSet)
router.register("videos", VideoItemViewSet)
router.register("media", MediaItemViewSet)


urlpatterns = [ path("", include(router.urls)),
                path("login/", login_view, name="login"), 
                 path("send-enquiry/", send_enquiry),
]


