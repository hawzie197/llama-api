from django.urls import path
from api.analyze.views import AnalyzeUrlView

urlpatterns = [path("", AnalyzeUrlView.as_view())]
