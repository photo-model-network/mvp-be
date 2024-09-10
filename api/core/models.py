from django.db import models
from api.accounts.models import User
from api.packages.models import Package


class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    interaction_type = models.CharField(
        max_length=50
    )  # 예: 'click', 'purchase', 'rating'
    interaction_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # 예: 평점
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "인터랙션"
        verbose_name_plural = "인터랙션"
