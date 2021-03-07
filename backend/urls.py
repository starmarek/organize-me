from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .api.views.auth_view import CustomTokenObtainPairView, logout_view

router = routers.DefaultRouter()
# router.register("messages", MessageViewSet)

urlpatterns = [
    path("", never_cache(TemplateView.as_view(template_name="index.html")), name="index"),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/logout/", logout_view, name="logout_view"),
    path("api/token/", CustomTokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]
