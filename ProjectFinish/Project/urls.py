from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from pereval import views
from pereval.views import PerevalsViewset
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = routers.DefaultRouter()
router.register(r'users', views.UsersViewset)
router.register(r'coords', views.CoordsViewset)
router.register(r'level', views.LevelViewset)
router.register(r'images', views.ImagesViewset)
router.register(r'submitData', views.PerevalsViewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # path('login/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger-ui/', TemplateView.as_view(
       template_name='swagger-ui.html',
       extra_context={'schema_url':'openapi-schema'}
   ), name='swagger-ui'),
]
