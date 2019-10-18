from django.urls import path, include

urlpatterns = [path("accounts/", include("api.accounts.urls"))]
urlpatterns = [path("analyze/", include("api.analyze.urls"))]
