from django.urls import include, path, re_path

from rest_framework import routers

from platform_app import views 


app_name = "platform_app"

router = routers.DefaultRouter()
router.register(r"platform", views.BasicViewSet, basename="basic API")

urlpatterns = [
    path('/', include(router.urls)),
]