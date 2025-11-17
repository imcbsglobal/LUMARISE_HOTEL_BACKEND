from django.contrib import admin
from .models import (
    Room, Booking, OfflineBooking, BookingRequest,
    UserProfile, Testimonial, VideoItem, Booking
)

models = [Room, Booking, OfflineBooking, BookingRequest, UserProfile, Testimonial, VideoItem]
for m in models:
    admin.site.register(m)

from .models import MediaItem

admin.site.register(MediaItem)

if not admin.site.is_registered(Booking):
    @admin.register(Booking)
    class BookingAdmin(admin.ModelAdmin):
        list_display = ('id', 'guest_name', 'check_in', 'check_out')
