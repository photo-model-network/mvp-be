from api.packages.models import Package, PackagePicture
import os, uuid
from django.core.files.storage import default_storage

def save_images(images, package):
    """이미지 여러장 저장"""
    image_objects = []
    for image in images:
        new_filename = save_image(image, package)
        image_objects.append(PackagePicture(package=package, image=new_filename))
    PackagePicture.objects.bulk_create(image_objects)

def save_image(image, package):
    """packages/{id}/images/uuid.ext 경로로 이미지 저장"""
    ext = os.path.splitext(image.name)[1]
    new_filename = os.path.join(
        f"packages/{package.id}/images", f"{uuid.uuid4()}{ext}"
    )
    default_storage.save(new_filename, image)
    return new_filename

def save_thumbnail(thumbnail, package):
    """packages/{id}/thumbnail/uuid.ext 경로로 썸네일 저장"""
    ext = os.path.splitext(thumbnail.name)[1]
    new_filename = os.path.join(
        f"packages/{package.id}/thumbnail", f"{uuid.uuid4()}{ext}"
    )
    default_storage.save(new_filename, thumbnail)
    package.thumbnail = new_filename
    package.save()
