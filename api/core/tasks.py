from celery import shared_task
from api.packages.models import Package
from api.core.models import Interaction
from api.accounts.models import User


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
        print(f"User with id {user_id} does not exist.")
    except Package.DoesNotExist:
        print(f"Package with id {package_id} does not exist.")
