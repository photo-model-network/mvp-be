from django.db import models
from api.common.models import CommonModel
from api.accounts.models import User
from api.packages.models import Package


class Review(CommonModel):
    """리뷰 (촬영 패키지 후기)"""

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.customer.username} : {self.comment}"

    class Meta:
        verbose_name = "리뷰 (촬영 패키지 후기)"
        verbose_name_plural = "리뷰 (촬영 패키지 후기)"

        ordering = ["-created_at"]
