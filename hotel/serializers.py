from rest_framework import serializers
from .models import (
    Room, Booking, OfflineBooking, BookingRequest,
    UserProfile, Testimonial, VideoItem, MediaItem, RoomImage,
)


# ✅ Serializer for RoomImage (multiple images)
class RoomImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = RoomImage
        fields = ["id", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            # ✅ Return the absolute URL only once
            return request.build_absolute_uri(obj.image.url)
        return None

# ✅ Serializer for Room with nested images
class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_main_image(self, obj):
        request = self.context.get("request")
        if obj.main_image and hasattr(obj.main_image, "url"):
            return request.build_absolute_uri(obj.main_image.url)
        return None

class BookingSerializer(serializers.ModelSerializer):
    class Meta: model = Booking; fields = "__all__"

class OfflineBookingSerializer(serializers.ModelSerializer):
    class Meta: model = OfflineBooking; fields = "__all__"

class BookingRequestSerializer(serializers.ModelSerializer):
    class Meta: model = BookingRequest; fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta: model = UserProfile; fields = "__all__"

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta: model = Testimonial; fields = "__all__"

class VideoItemSerializer(serializers.ModelSerializer):
    class Meta: model = VideoItem; fields = "__all__"

class MediaItemSerializer(serializers.ModelSerializer):
    class Meta: model = MediaItem; fields = "__all__"



