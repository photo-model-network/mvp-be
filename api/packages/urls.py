from django.urls import path

from .views import *

urlpatterns = [
    path("packages/create/", PackageCreateView.as_view(), name='package_create'),
    path("packages/", PackageListView.as_view(), name='package_list'),
    path("packages/<str:pk>/", PackageDetailView.as_view(), name='package_detail'),
    path("packages/<str:pk>/update/", PackageUpdateView.as_view(), name='package_update'),
    path("packages/<str:pk>/delete/", PackageDeleteView.as_view(), name='package_delete'),
]