from django.db import models
# from shortuuid.django_fields import ShortUUIDField

# Create your models here.
class CommonModel(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
