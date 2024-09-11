from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from conf.elasticsearch import es
from .models import Package


def index_package(package):
    doc = {
        "title": package.title,
        "category": package.category,
        "provider_id": package.provider.id,
        "provider_name": package.provider.name,
        "summary": package.summary,
        "html_content": package.html_content,
        "tags": [tag.name for tag in package.tags.all()],
        "average_rating": package.average_rating,
    }

    es.index(index="packages", id=package.id, body=doc)


@receiver(post_save, sender=Package)
def save_package_to_es(sender, instance, **kwargs):
    index_package(instance)


@receiver(post_delete, sender=Package)
def delete_package_from_es(sender, instance, **kwargs):
    es.delete(index="packages", id=instance.id)
