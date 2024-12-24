from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('system', views.SystemMetricsViewSet)
router.register('application', views.AppMetricsViewSet)
router.register('rules', views.AlertRuleViewSet)
router.register('alerts', views.AlertHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('alert/webhook/', views.AlertWebhookView.as_view(), name='alert-webhook'),
]