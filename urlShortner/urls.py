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
    path('', index, name='home'),
    path('registration/', registration, name='registration'),
    path('settings/', settings_, name='configs'),
    path('report/', report, name='report'),
    path('stats/<str:url_id>', stats, name='stats'),
    path('verify/<str:verify_id>', verify),
    path('<str:url_id>/', handle_link),

    # include RESTful API routes
    path('api/v1/', include('Api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
