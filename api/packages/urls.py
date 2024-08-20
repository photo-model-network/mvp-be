from django.urls import path

from .views import *

urlpatterns = [
    path("packages/", PackageListView.as_view(), name='package_list'),
    path("packages/new/", PackageCreateView.as_view(), name='package_create'),
    path("packages/<str:pk>/", PackageDetailView.as_view(), name='package_detail'),
    path("packages/<str:pk>/update/", PackageUpdateView.as_view(), name='package_update'),
    path("packages/<str:pk>/delete/", PackageDeleteView.as_view(), name='package_delete'),
    path("packages/approved/", ProviderPackagesListView.as_view(), name='approved_user_packages'),
]