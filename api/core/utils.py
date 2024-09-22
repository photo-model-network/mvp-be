from api.packages.models import PackagePicture
from api.reviews.models import ReviewPicture
import os, uuid
from django.core.files.storage import default_storage

def save_package_images(images, package):
    """packages/{id}/images/uuid.ext 경로로 이미지 저장"""
    image_objects = []
    for image in images:
        ext = os.path.splitext(image.name)[1]
        new_filename = os.path.join(
            f"packages/{package.id}/images", f"{uuid.uuid4()}{ext}"
        )
        default_storage.save(new_filename, image)
        image_objects.append(PackagePicture(package=package, image=new_filename))
    PackagePicture.objects.bulk_create(image_objects)

def save_thumbnail(thumbnail, package):
    """packages/{id}/thumbnail/uuid.ext 경로로 썸네일 저장"""
    ext = os.path.splitext(thumbnail.name)[1]
    new_filename = os.path.join(
        f"packages/{package.id}/thumbnail", f"{uuid.uuid4()}{ext}"
    )
    default_storage.save(new_filename, thumbnail)
    package.thumbnail = new_filename
    package.save()

def save_review_images(images, review):
    """reviews/{id}/images/uuid.ext 경로로 이미지 저장"""
    image_objects = []
    for image in images:
        ext = os.path.splitext(image.name)[1]
        new_filename = os.path.join(
            f"reviews/{review.id}/images", f"{uuid.uuid4()}{ext}"
        )
        default_storage.save(new_filename, image)
        image_objects.append(ReviewPicture(review=review, image=new_filename))
    ReviewPicture.objects.bulk_create(image_objects)