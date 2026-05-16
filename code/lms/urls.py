"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from lms.api import api, apiv1
from django.conf import settings
from django.conf.urls.static import static

apiv1_urls = apiv1.urls
api_urls = api.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),

    # OLD ROUTES (backward compatibility)
    path("api/", apiv1_urls),
    path("api/protected/", api_urls),

    # VERSIONED ROUTES
    path("api/v1/", apiv1_urls),
    path("api/v1/protected/", api_urls),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)