from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from hotel.utils import compress_image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import sys

class R2MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    default_acl = 'public-read'

    @property
    def bucket_name(self):
        return settings.CLOUDFLARE_R2_BUCKET_NAME

    @property
    def custom_domain(self):
        return settings.CLOUDFLARE_R2_PUBLIC_URL

    @property
    def endpoint_url(self):
        return settings.CLOUDFLARE_R2_ENDPOINT

    def _save(self, name, content):
        if hasattr(content, "content_type") and "image" in content.content_type:
            compressed_file = compress_image(content)
            content = compressed_file

        return super()._save(name, content)
