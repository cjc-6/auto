from rest_framework import serializers
from .models import SystemMetrics, AppMetrics, AlertRule, AlertHistory

class SystemMetricsSerializer(serializers.ModelSerializer):
    """系统指标序列化器"""
    class Meta:
        model = SystemMetrics
        fields = '__all__'

class AppMetricsSerializer(serializers.ModelSerializer):
    """应用指标序列化器"""
    class Meta:
        model = AppMetrics
        fields = '__all__'

class AlertRuleSerializer(serializers.ModelSerializer):
    """告警规则序列化器"""
    notification_display = serializers.SerializerMethodField()

    class Meta:
        model = AlertRule
        fields = '__all__'

    def get_notification_display(self, obj):
        """获取通知方式的显示文本"""
        notification_map = {
            'email': '邮件',
            'sms': '短信',
            'phone': '电话'
        }
        return [notification_map.get(n, n) for n in obj.notification]

class AlertHistorySerializer(serializers.ModelSerializer):
    """告警历史序列化器"""
    rule_name = serializers.CharField(source='rule.name', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AlertHistory
        fields = '__all__'

class AlertHistoryCreateSerializer(serializers.ModelSerializer):
    """告警历史创建序列化器"""
    class Meta:
        model = AlertHistory
        fields = ['target', 'content', 'level', 'rule']

class AlertHistoryUpdateSerializer(serializers.ModelSerializer):
    """告警历史更新序列化器"""
    class Meta:
        model = AlertHistory
        fields = ['status', 'confirmer', 'confirm_time', 'resolver', 'resolve_time', 'comment']
        read_only_fields = ['alert_time', 'target', 'content', 'level', 'rule']