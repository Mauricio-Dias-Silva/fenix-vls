from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/telemetry/', views.get_telemetry, name='get_telemetry'),
    path('api/set_focus/', views.set_focus, name='set_focus'),
    path('api/set_frequency/', views.set_frequency, name='set_frequency'),
]
