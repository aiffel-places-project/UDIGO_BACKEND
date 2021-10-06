from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="UDIGO API",
      default_version='v1',
      description="UDIGO API DOCUMENT",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="namji117@gmail.com"),
      license=openapi.License(name="License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

project_apps = [
    path("place", include("place.urls")),
    path("user", include("user.urls")),
]

urlpatterns = urlpatterns + project_apps

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)