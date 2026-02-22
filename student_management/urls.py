from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

handler403 = 'students.views.error_403'
handler404 = 'students.views.error_404'

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('',            RedirectView.as_view(url='/accounts/login/')),
    path('accounts/',   include('accounts.urls')),
    path('dashboard/',  include('students.dashboard_urls')),
    path('students/',   include('students.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
