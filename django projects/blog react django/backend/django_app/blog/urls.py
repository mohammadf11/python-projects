from rest_framework import routers
from . import views

router = routers.SimpleRouter()

router.register("", views.PostViewSet)

urlpatterns= router.urls
