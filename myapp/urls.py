from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('purchase_or_sale/', views.purchase_or_sale, name='purchase_or_sale'),
    path('report/', views.report_view, name='report_view'),
    path('logout/', views.logout_view, name='logout'),
    path('download-csv/', views.download_csv, name='download_csv'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
