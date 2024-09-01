from django.urls import path
from batches_app.views import BatchesViewSet
from rest_framework import routers

app_name = "batches_app"

router = routers.SimpleRouter()

router.register(r"batches", BatchesViewSet, basename="batches")

urlpatterns = router.urls
