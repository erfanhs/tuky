from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

from main.views import *

urlpatterns = [

    # admin panel
    path('admin/', admin.site.urls),

    # site routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('registration/', TemplateView.as_view(template_name='registration.html'), name='registration'),
    path('settings/', TemplateView.as_view(template_name='settings.html'), name='configs'),
    path('report/', TemplateView.as_view(template_name='report.html'), name='report'),
    path('stats/<str:url_id>', TemplateView.as_view(template_name='stats.html'), name='stats'),
    path('verify/<str:verify_id>', verify),
    path('<str:url_id>/', handle_link),

    # include RESTful API routes
    path('api/v1/', include('Api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)