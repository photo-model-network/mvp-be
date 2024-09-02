from celery import shared_task
from api.packages.models import Package
from api.accounts.models import User
from .models import Interaction

import logging

logger = logging.getLogger(__name__)


@shared_task
def save_interaction(user_id, package_id, interaction_type, interaction_value=None):
    try:
        user = User.objects.get(id=user_id)
        package = Package.objects.get(id=package_id)
        Interaction.objects.create(
            user=user,
            package=package,
            interaction_type=interaction_type,
            interaction_value=interaction_value,
        )

    except User.DoesNotExist:
        logging.info(f"유저 ID {user_id}를 찾을 수 없습니다.")
    except Package.DoesNotExist:
        logging.warning(f"패키지 ID {package_id}를 찾을 수 없습니다.")
