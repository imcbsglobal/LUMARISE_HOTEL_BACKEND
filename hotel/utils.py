from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile

def compress_image(uploaded_file, quality=40, max_width=1600):
    try:
        # Open image safely
        img = Image.open(uploaded_file)

        # Fix rotation issues from mobile cameras (EXIF)
        img = ImageOps.exif_transpose(img)

        # Convert all images to RGB (required for WEBP)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize if too large
        width, height = img.size
        if width > max_width:
            new_height = int(height * (max_width / width))
            img = img.resize((max_width, new_height), Image.LANCZOS)

        # Remove metadata (saves 100–150 KB)
        img_without_meta = Image.new(img.mode, img.size)
        img_without_meta.putdata(list(img.getdata()))

        buffer = BytesIO()

        # Save as WEBP (best compression)
        img_without_meta.save(
            buffer,
            format="WEBP",
            optimize=True,
            quality=quality,
        )
        buffer.seek(0)

        # Rename file extension
        filename = uploaded_file.name.rsplit(".", 1)[0] + ".webp"

        return ContentFile(buffer.read(), name=filename)

    except Exception as e:
        print("Compression error:", e)
        return uploaded_file
