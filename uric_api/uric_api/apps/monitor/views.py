from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count, Avg
from datetime import timedelta
import random
from rest_framework.views import APIView
import json

from .models import SystemMetrics, AppMetrics, AlertRule, AlertHistory
from .serializers import (
    SystemMetricsSerializer, AppMetricsSerializer,
    AlertRuleSerializer, AlertHistorySerializer,
    AlertHistoryCreateSerializer, AlertHistoryUpdateSerializer
)

class SystemMetricsViewSet(ModelViewSet):
    """系统指标视图集"""
    queryset = SystemMetrics.objects.all()
    serializer_class = SystemMetricsSerializer

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """获取系统概览数据"""
        total_servers = self.queryset.values('server').distinct().count()
        normal_servers = self.queryset.filter(
            cpu_usage__lt=80,
            memory_usage__lt=80,
            disk_usage__lt=80
        ).values('server').distinct().count()
        warning_servers = self.queryset.filter(
            cpu_usage__gte=80,
            cpu_usage__lt=90
        ).values('server').distinct().count()
        critical_servers = total_servers - normal_servers - warning_servers

        return Response({
            'total': total_servers,
            'normal': normal_servers,
            'warning': warning_servers,
            'critical': critical_servers,
            'uptime_rate': round((normal_servers + warning_servers) / total_servers * 100, 1) if total_servers > 0 else 0
        })

    @action(detail=False, methods=['get'])
    def trends(self, request):
        """获取性能趋势数据"""
        hours = int(request.query_params.get('hours', 24))
        start_time = timezone.now() - timedelta(hours=hours)
        
        metrics = self.queryset.filter(created_time__gte=start_time)
        data = {
            'timestamps': [],
            'cpu': [],
            'memory': [],
            'disk': []
        }
        
        # 模拟数据，实际应该从数据库聚合
        for i in range(hours):
            timestamp = start_time + timedelta(hours=i)
            data['timestamps'].append(timestamp.strftime('%H:00'))
            data['cpu'].append(random.uniform(30, 70))
            data['memory'].append(random.uniform(40, 70))
            data['disk'].append(random.uniform(60, 80))
        
        return Response(data)

class AppMetricsViewSet(ModelViewSet):
    """应用指标视图集"""
    queryset = AppMetrics.objects.all()
    serializer_class = AppMetricsSerializer

    @action(detail=False, methods=['get'])
    def performance(self, request):
        """获取应用性能数据"""
        app_name = request.query_params.get('app_name')
        time_range = request.query_params.get('time_range', '1h')
        
        # 根据时间范围获取开始时间
        now = timezone.now()
        if time_range == '30min':
            start_time = now - timedelta(minutes=30)
        elif time_range == '1h':
            start_time = now - timedelta(hours=1)
        elif time_range == '6h':
            start_time = now - timedelta(hours=6)
        else:  # 24h
            start_time = now - timedelta(hours=24)

        # 获取性能数据，这里使用模拟数据
        return Response({
            'qps': random.uniform(800, 1500),
            'avg_response_time': random.uniform(100, 200),
            'error_rate': random.uniform(0.1, 0.5),
            'concurrent_connections': random.randint(100, 500)
        })

    @action(detail=False, methods=['get'])
    def apis(self, request):
        """获取API调用统计"""
        # 模拟数据，实际应该从数据库获取
        return Response([
            {
                'path': '/api/v1/orders',
                'count': random.randint(10000, 20000),
                'avgRt': f'{random.randint(80, 150)}ms',
                'maxRt': f'{random.randint(300, 600)}ms',
                'errorCount': random.randint(10, 50),
                'status': '正常' if random.random() > 0.2 else '异常'
            } for _ in range(10)
        ])

class AlertRuleViewSet(ModelViewSet):
    """告警规则视图集"""
    queryset = AlertRule.objects.all()
    serializer_class = AlertRuleSerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """切换规则状态"""
        rule = self.get_object()
        rule.status = 'disabled' if rule.status == 'enabled' else 'enabled'
        rule.save()
        return Response({'status': rule.status})

class AlertHistoryViewSet(ModelViewSet):
    """告警历史视图集"""
    queryset = AlertHistory.objects.all()
    serializer_class = AlertHistorySerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AlertHistoryCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AlertHistoryUpdateSerializer
        return AlertHistorySerializer

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取告警统计数据"""
        today = timezone.now().date()
        today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        
        total_today = self.queryset.filter(alert_time__gte=today_start).count()
        unconfirmed = self.queryset.filter(status='unconfirmed').count()
        confirmed = self.queryset.filter(status='confirmed').count()
        resolved = self.queryset.filter(status='resolved').count()

        return Response({
            'total_today': total_today,
            'unconfirmed': unconfirmed,
            'confirmed': confirmed,
            'resolved': resolved
        })

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """确认告警"""
        alert = self.get_object()
        if alert.status != 'unconfirmed':
            return Response({'detail': '只能确认未确认的告警'}, status=status.HTTP_400_BAD_REQUEST)
        
        alert.status = 'confirmed'
        alert.confirmer = request.user.username
        alert.confirm_time = timezone.now()
        alert.save()
        
        return Response(AlertHistorySerializer(alert).data)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """解决告警"""
        alert = self.get_object()
        if alert.status == 'resolved':
            return Response({'detail': '告警已解决'}, status=status.HTTP_400_BAD_REQUEST)
        
        alert.status = 'resolved'
        alert.resolver = request.user.username
        alert.resolve_time = timezone.now()
        alert.comment = request.data.get('comment', '')
        alert.save()
        
        return Response(AlertHistorySerializer(alert).data)

class AlertWebhookView(APIView):
    def post(self, request):
        try:
            alerts = request.data.get('alerts', [])
            for alert in alerts:
                status = 'firing' if alert['status'] == 'firing' else 'resolved'
                alert_data = {
                    'alert_name': alert['labels'].get('alertname'),
                    'alert_status': status,
                    'alert_level': alert['labels'].get('severity', 'warning'),
                    'alert_info': alert['annotations'].get('description'),
                    'alert_target': alert['labels'].get('instance', 'unknown')
                }
                
                serializer = AlertHistorySerializer(data=alert_data)
                if serializer.is_valid():
                    serializer.save()
                
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)