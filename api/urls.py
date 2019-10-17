from django.urls import path, include

urlpatterns = [path("accounts/", include("api.accounts.urls"))]
