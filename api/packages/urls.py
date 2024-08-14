from django.urls import path

from .views import *

urlpatterns = [
    path("packages/", PackageCreateView.as_view(), name='package_create'),
    path("packages/", PackageListView.as_view(), name='package_list'),
    path("packages/<str:pk>/", PackageDetailView.as_view(), name='package_detail'),
    path("packages/<str:pk>/", PackageUpdateView.as_view(), name='package_update'),
    path("packages/<str:pk>/", PackageDeleteView.as_view(), name='package_delete'),
]