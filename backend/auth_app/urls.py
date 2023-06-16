from django.urls import include, path, re_path

from rest_framework import routers

from auth_app import views


app_name = "auth_app"

router = routers.DefaultRouter()
router.register(r"auth", views.BasicViewSet, basename="basic API")

urlpatterns = [
    path("/", include(router.urls)),
    path("/signup", views.SignUpView.as_view(), name="SignUp"),
]
