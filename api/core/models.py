from django.db import models
from api.accounts.models import User
from api.common.models import CommonModel


class Preference(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 유저별로 선호도를 알 수 있는 것들 저장
