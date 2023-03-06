"""servidor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from interactions.views import InteractionsViewSet

# API Router v1
router = routers.SimpleRouter()
router.register(r'interacoes', InteractionsViewSet, base_name='interaction')

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # API v1 ENDPOINTS
    url(r'^v1/', include(router.urls, namespace='v1')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
