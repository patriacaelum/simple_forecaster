from django.urls import path

from forecaster import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.create_forecast, name="new"),
    path("create", views.create, name="create"),
    path("graph-data", views.normal_distribution, name="graph-data"),
    path("recent", views.recent, name="recent"),
]
