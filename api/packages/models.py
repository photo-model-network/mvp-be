from django.db import models
from api.common.models import CommonModel
from api.accounts.models import User
# Create your models here.
class Package(CommonModel):

    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    thumbnail = models.URLField()
    intro_video = models.URLField()
    location = models.CharField(max_length=100)
    summary = models.TextField()
    content = models.TextField()
    # tags = 

    def __str__(self):
        return self.title
        