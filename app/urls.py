from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.routers import DefaultRouter

from serv.api.photos import PhotoView
from serv.api.toplist import TopListView
from serv.api.users import CreateUserView, LoginUserView

schema_view = get_schema_view(
    openapi.Info(
        title="App API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
    authentication_classes=(BasicAuthentication,),
)

router = DefaultRouter()

router.register(r"user", CreateUserView, basename="user")
router.register(r"login", LoginUserView, basename="login_user")
router.register(r"photo", PhotoView, basename="photo")
router.register(r"toplist", TopListView, basename="toplist")

urlpatterns = [
    url(r"^api/v1/", include(router.urls)),
    url(r"^admin/", admin.site.urls),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
