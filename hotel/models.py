from django.db import models
from django.utils import timezone
from datetime import date

# ===== Rooms (BookManagement.jsx) =====
class Room(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, default="")
    guests = models.CharField(max_length=100, blank=True, default="")
    bed = models.CharField(max_length=100, blank=True, default="")
    view = models.CharField(max_length=100, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desc = models.TextField(blank=True, default="")

    # Single representative image
    main_image = models.ImageField(upload_to="rooms/", null=True, blank=True)

    # Store multiple images (related via foreign key)
    # You’ll need to create a secondary model for this:
    def __str__(self):
        return self.title


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="rooms/gallery/")

    def __str__(self):
        return f"Image for {self.room.title}"

# ===== Online bookings =====
class Booking(models.Model):
    guest_name = models.CharField(max_length=100, default="Guest")
    name = models.CharField(max_length=100, blank=True, default="")
    email = models.EmailField(default="guest@example.com")
    phone = models.CharField(max_length=20, default="0000000000")

    room_type = models.CharField(max_length=100, default="Standard Room")
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL, related_name="bookings")
    room_number = models.CharField(max_length=10, blank=True, null=True)

    # ✅ Corrected date defaults
    check_in = models.DateField(default=date.today)
    check_out = models.DateField(default=date.today)
    checkin = models.DateField(null=True, blank=True)
    checkout = models.DateField(null=True, blank=True)

    guests = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=50,
        default="Pending",
        choices=[
            ("Pending", "Pending"),
            ("Confirmed", "Confirmed"),
            ("Checked-in", "Checked-in"),
            ("Checked-out", "Checked-out"),
            ("Cancelled", "Cancelled"),
        ],
    )

    # ✅ Fix this one too
    booking_date = models.DateField(default=date.today)
    special_requests = models.TextField(blank=True, default="")
    id_number = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        from datetime import datetime
        # Ensure datetime values get converted to date
        for field_name in ["check_in", "check_out", "checkin", "checkout"]:
            val = getattr(self, field_name)
            if isinstance(val, datetime):
                setattr(self, field_name, val.date())

        # Sync names
        if self.name and not self.guest_name:
            self.guest_name = self.name
        elif self.guest_name and not self.name:
            self.name = self.guest_name

        # Sync dates
        if self.checkin:
            self.check_in = self.checkin
        if self.checkout:
            self.check_out = self.checkout
        elif self.check_in and not self.checkin:
            self.checkin = self.check_in
        if self.check_out and not self.checkout:
            self.checkout = self.check_out

        super().save(*args, **kwargs)

    def __str__(self):
        display_name = self.name or self.guest_name
        return f"{display_name} ({self.room_type})"

    @property
    def days(self):
        check_in_date = self.checkin or self.check_in
        check_out_date = self.checkout or self.check_out
        return (check_out_date - check_in_date).days


# ===== Offline bookings =====
class OfflineBooking(models.Model):
    guest_name = models.CharField(max_length=100, default="Guest")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=20, default="0000000000")
    room_type = models.CharField(max_length=100, default="Standard Room")

    # ✅ Fix these
    check_in = models.DateField(default=date.today)
    check_out = models.DateField(default=date.today)
    booking_date = models.DateField(default=date.today)

    guests = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default="Confirmed")
    booking_type = models.CharField(max_length=20, default="Walk-in")
    created_by = models.CharField(max_length=100, default="Admin")
    payment_method = models.CharField(max_length=50, default="Cash")
    id_verified = models.BooleanField(default=False)
    special_requests = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.guest_name} ({self.booking_type})"


# ===== Booking requests =====
class BookingRequest(models.Model):
    guest_name = models.CharField(max_length=100, default="Guest")
    email = models.EmailField(default="guest@example.com")
    phone = models.CharField(max_length=20, default="0000000000")
    room_type = models.CharField(max_length=100, default="Standard Room")

    # ✅ Fix all these too
    check_in = models.DateField(default=date.today)
    check_out = models.DateField(default=date.today)
    request_date = models.DateField(default=date.today)

    guests = models.PositiveIntegerField(default=1)
    estimated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default="Pending")
    priority = models.CharField(max_length=20, default="Normal")
    source = models.CharField(max_length=50, default="Website")
    response_deadline = models.DateField(null=True, blank=True)
    special_requests = models.TextField(blank=True, default="")
    guest_notes = models.TextField(blank=True, default="")
    admin_notes = models.TextField(blank=True, default="")
    assigned_to = models.CharField(max_length=100, default="Unassigned")

    def __str__(self):
        return f"Request: {self.guest_name} - {self.status}"


# ===== Registered users =====
class UserProfile(models.Model):
    name = models.CharField(max_length=100, default="User")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, default="0000000000")

    # ✅ Fix this
    join_date = models.DateField(default=date.today)
    last_login = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, default="Active")
    bookings = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.name


# ===== Testimonials =====
class Testimonial(models.Model):
    name = models.CharField(max_length=100, default="Anonymous")
    role = models.CharField(max_length=100, blank=True, default="")
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(default="")

    # ✅ Fix this too
    date = models.DateField(default=date.today)

    avatar = models.ImageField(upload_to="testimonials/", null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.rating})"


# ===== Video Gallery =====
class VideoItem(models.Model):
    title = models.CharField(max_length=200, default="Untitled Video")
    category = models.CharField(max_length=100, default="General")

    # ✅ Fix upload_date
    upload_date = models.DateField(default=date.today)

    duration = models.CharField(max_length=10, blank=True, default="")
    status = models.CharField(max_length=20, default="Draft")
    file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)

    def __str__(self):
        return self.title


class MediaItem(models.Model):
    MEDIA_TYPES = (
        ("image", "Image"),
        ("video", "Video"),
    )

    title = models.CharField(max_length=100)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default="image")
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    video = models.FileField(upload_to="videos/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.media_type})"
