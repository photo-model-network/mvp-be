from django.urls import path

from .views import ReviewCreateListView, ReviewUpdateDeleteView

urlpatterns = [
    path("packages/<str:packages_id>/reviews/", ReviewCreateListView.as_view(), name='review_create_listview'),
    path("packages/<str:packages_id>/reviews/<str:id>", ReviewUpdateDeleteView.as_view(), name='review_update_delete'),
]