from xml.dom.minidom import Document
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.main.urls", namespace='main')),
    path("accounting/", include("apps.accounting.urls", namespace='accounting')),
    path("products/", include("apps.products.urls", namespace='products')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)