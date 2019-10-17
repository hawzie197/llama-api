from django.urls import path
from api.accounts.views import UserViewSet, GroupViewSet

urlpatterns = [
    path("users/", UserViewSet.as_view({"get": "list"})),
    path("groups/", GroupViewSet.as_view({"get": "list"})),
]
