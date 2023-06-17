from django.urls import include, path, re_path

from rest_framework import routers

from auth_app.views import *


app_name = "auth_app"

# router = routers.DefaultRouter()
# router.register(r"auth", views.BasicViewSet, basename="basic API")

urlpatterns = [
    # path("/", include(router.urls)),
    path("/signup", SignUpView.as_view(), name="SignUp"),
    path("/signin", SignInView.as_view(), name="SignIn"),
]
