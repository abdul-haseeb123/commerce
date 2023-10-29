from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", views.api_root, name="api-root"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("users/", views.UserList.as_view(), name='user-list'),
    path("users/<int:pk>/", views.UserDetail.as_view(), name='user-detail'),
    path("listings/", views.ListingList.as_view(), name='listing-list'),
    path("listings/<int:pk>/", views.ListingDetail.as_view(), name='listing-detail'),
    path("listings/<int:pk>/bids/", views.BidList.as_view(), name='bid-list'),
    path("listings/<int:pk>/comments/", views.CommentList.as_view(), name='comment-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)