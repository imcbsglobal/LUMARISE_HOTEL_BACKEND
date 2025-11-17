from rest_framework import viewsets, filters
from .models import (
    Room, Booking, OfflineBooking, BookingRequest,
    UserProfile, Testimonial, VideoItem
)
from .serializers import (
    RoomSerializer, BookingSerializer, OfflineBookingSerializer, BookingRequestSerializer,
    UserProfileSerializer, TestimonialSerializer, VideoItemSerializer, RoomImage
)

class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id"]       # override per model as needed
    ordering_fields = ["id",]    # override per model as needed
    ordering = ["-id"]

# paste this in place of your current RoomViewSet
class RoomViewSet(BaseViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    search_fields = ["title", "price"]
    ordering_fields = ["price", "id"]

    def perform_main_image(self, room, files):
        # If no main_image on the model, set first uploaded file as main_image
        if not room.main_image and files:
            first = files[0]
            room.main_image.save(first.name, first, save=True)

    def create(self, request, *args, **kwargs):
        from rest_framework import status
        from rest_framework.response import Response
        from django.db import transaction
        import traceback

        try:
            # DON'T deep-copy request.data — files break deepcopy
            data = request.data
            print("📸 FILES RECEIVED:", request.FILES)
            files = request.FILES.getlist("images")
            main_img = request.FILES.get("main_image")

            with transaction.atomic():
                # let serializer process form fields; we pass request context so serializer can build absolute URIs
                serializer = self.get_serializer(data=data, context={"request": request})
                serializer.is_valid(raise_exception=True)
                room = serializer.save()

                # If main_image file uploaded, save it explicitly to the model field
                if main_img:
                    room.main_image.save(main_img.name, main_img, save=True)

                # Save any additional images
                for f in files:
                    RoomImage.objects.create(room=room, image=f)

                # If still no main_image, set first of files as main_image
                self.perform_main_image(room, files)

            return Response(self.get_serializer(room, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            print("❌ ERROR IN ROOM CREATE:", e)
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)

    def update(self, request, *args, **kwargs):
        from django.db import transaction
        from rest_framework.response import Response
        import traceback, json

        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            data = request.data
            files = request.FILES.getlist("images")
            main_img = request.FILES.get("main_image")

            with transaction.atomic():

                # ✅ 1. DELETE SELECTED OLD IMAGES
                deleted_list = data.get("deleted_images")
                if deleted_list:
                    try:
                        ids = json.loads(deleted_list)
                        RoomImage.objects.filter(id__in=ids, room=instance).delete()
                    except Exception as e:
                        print("❌ DELETE IMAGE ERROR:", e)

                # ✅ 2. UPDATE TEXT FIELDS
                serializer = self.get_serializer(
                    instance, data=data, partial=partial,
                    context={"request": request}
                )
                serializer.is_valid(raise_exception=True)
                room = serializer.save()

                # ✅ 3. IF NEW MAIN IMAGE, REPLACE IT
                if main_img:
                    room.main_image.save(main_img.name, main_img, save=True)

                # ✅ 4. ADD NEW GALLERY IMAGES
                for f in files:
                    RoomImage.objects.create(room=room, image=f)

                # Ensure main image exists
                self.perform_main_image(room, files)

            return Response(self.get_serializer(room, context={"request": request}).data)

        except Exception as e:
            print("❌ ERROR IN ROOM UPDATE:", e)
            traceback.print_exc()
            return Response({"error": str(e)}, status=500)


class BookingViewSet(BaseViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    search_fields = ["guest_name", "email", "phone", "room_type", "status"]
    ordering_fields = ["booking_date", "check_in", "check_out", "total_amount"]

class OfflineBookingViewSet(BaseViewSet):
    queryset = OfflineBooking.objects.all()
    serializer_class = OfflineBookingSerializer
    search_fields = ["guest_name", "phone", "room_type", "status", "booking_type", "created_by"]
    ordering_fields = ["booking_date", "check_in", "check_out", "total_amount"]

class BookingRequestViewSet(BaseViewSet):
    queryset = BookingRequest.objects.all()
    serializer_class = BookingRequestSerializer
    search_fields = ["guest_name", "email", "status", "priority", "source"]
    ordering_fields = ["request_date", "response_deadline", "estimated_amount"]

class UserProfileViewSet(BaseViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    search_fields = ["name", "email", "phone", "status"]
    ordering_fields = ["join_date", "last_login", "bookings"]

class TestimonialViewSet(BaseViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    search_fields = ["name", "role", "comment"]
    ordering_fields = ["date", "rating"]

class VideoItemViewSet(BaseViewSet):
    queryset = VideoItem.objects.all()
    serializer_class = VideoItemSerializer
    search_fields = ["title", "category", "status"]
    ordering_fields = ["upload_date"]

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
from .models import MediaItem
from .serializers import MediaItemSerializer

class MediaItemViewSet(viewsets.ModelViewSet):
    queryset = MediaItem.objects.all().order_by('-uploaded_at')
    serializer_class = MediaItemSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking

@api_view(["POST"])
def confirm_booking(request, booking_id):
    """
    Mark a booking as confirmed (used if admin confirms via WhatsApp)
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = "Confirmed"
        booking.save()
        return Response({"message": "Booking confirmed successfully!"})
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found"}, status=404)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

@api_view(["POST"])
def send_enquiry(request):
    try:
        name = request.data.get("name")
        place = request.data.get("place")
        email = request.data.get("email")
        phone = request.data.get("phone")
        message = request.data.get("message")

        subject = f"New Enquiry from {name}"
        body = f"""
        Name: {name}
        Place: {place}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """

        # use EmailMessage to add reply-to header
        mail = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            ["lumarisehotels@gmail.com"],  # where it should arrive
            reply_to=[email] if email else None,
        )
        mail.send(fail_silently=False)

        return Response({"success": "Email sent successfully!"}, status=200)

    except Exception as e:
        print("Error sending enquiry:", e)
        return Response({"error": "Failed to send email"}, status=500)

