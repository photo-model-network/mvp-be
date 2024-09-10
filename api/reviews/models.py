from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.common.models import CommonModel
from api.accounts.models import User
from api.packages.models import Package


class Review(CommonModel):
    """리뷰 (촬영 패키지 후기)"""

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    rating = models.DecimalField(
        max_digits=3,  # 최대 자릿수 (정수부 + 소수부)
        decimal_places=1,  # 소수점 이하 자릿수
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="0에서 5 사이의 소수로 평점을 매깁니다."
    )

    def __str__(self):
        return f"{self.customer.username} : {self.comment} ({self.rating}점)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.package.update_average_rating()

    def delete(self, *args, **kwargs):
        package = self.package
        super().delete(*args, **kwargs)
        package.update_average_rating()
        
    class Meta:
        verbose_name = "리뷰 (촬영 패키지 후기)"
        verbose_name_plural = "리뷰 (촬영 패키지 후기)"
        
        ordering = ["-created_at"]