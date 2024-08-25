from django.urls import path
from .views import StudioListView

urlpatterns = [
    path("studios/", StudioListView.as_view(), name="studio_list"),
]
