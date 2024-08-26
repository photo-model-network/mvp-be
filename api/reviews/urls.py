from django.urls import path

from .views import ReviewCreateView, ReviewListView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path(
        "packages/<str:package_id>/reviews/",
        ReviewListView.as_view(),
        name="review_listview",
    ),
    path(
        "packages/<str:package_id>/reviews/new/",
        ReviewCreateView.as_view(),
        name="review_create",
    ),
    path(
        "packages/<str:package_id>/reviews/<str:pk>/update/",
        ReviewUpdateView.as_view(),
        name="review_update",
    ),
    path(
        "packages/<str:package_id>/reviews/<str:pk>/delete/",
        ReviewDeleteView.as_view(),
        name="review_delete",
    ),
]
