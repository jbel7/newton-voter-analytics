from django.urls import include, path

urlpatterns = [
    path("", include("voter_analytics.urls")),
]
