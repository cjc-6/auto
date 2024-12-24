from django.db import models
from django.utils import timezone

class SystemMetrics(models.Model):
    """系统指标数据模型"""
    server = models.CharField(max_length=100, verbose_name='服务器')
    cpu_usage = models.FloatField(verbose_name='CPU使用率')
    memory_usage = models.FloatField(verbose_name='内存使用率')
    disk_usage = models.FloatField(verbose_name='磁盘使用率')
    network_rx = models.FloatField(verbose_name='网络接收速率')
    network_tx = models.FloatField(verbose_name='网络发送速率')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        db_table = 'monitor_system_metrics'
        verbose_name = '系统指标'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

class AppMetrics(models.Model):
    """应用指标数据模型"""
    app_name = models.CharField(max_length=100, verbose_name='应用名称')
    qps = models.FloatField(verbose_name='每秒请求数')
    response_time = models.FloatField(verbose_name='响应时间')
    error_rate = models.FloatField(verbose_name='错误率')
    instance_count = models.IntegerField(verbose_name='实例数')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    class Meta:
        db_table = 'monitor_app_metrics'
        verbose_name = '应用指标'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

class AlertRule(models.Model):
    """告警规则数据模型"""
    LEVEL_CHOICES = (
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
    )
    STATUS_CHOICES = (
        ('enabled', '启用'),
        ('disabled', '禁用'),
    )

    name = models.CharField(max_length=100, verbose_name='规则名称')
    target = models.CharField(max_length=100, verbose_name='监控对象')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name='告警级别')
    metric = models.CharField(max_length=50, verbose_name='监控指标')
    operator = models.CharField(max_length=10, verbose_name='比较运算符')
    threshold = models.FloatField(verbose_name='阈值')
    duration = models.IntegerField(verbose_name='持续时间')
    notification = models.JSONField(verbose_name='通知方式')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='enabled', verbose_name='状态')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'monitor_alert_rule'
        verbose_name = '告警规则'
        verbose_name_plural = verbose_name
        ordering = ['-updated_time']

class AlertHistory(models.Model):
    """告警历史数据模型"""
    LEVEL_CHOICES = (
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
    )
    STATUS_CHOICES = (
        ('unconfirmed', '未确认'),
        ('confirmed', '已确认'),
        ('resolved', '已解决'),
    )

    alert_time = models.DateTimeField(default=timezone.now, verbose_name='告警时间')
    target = models.CharField(max_length=100, verbose_name='告警对象')
    content = models.TextField(verbose_name='告警内容')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name='告警级别')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unconfirmed', verbose_name='状态')
    rule = models.ForeignKey(AlertRule, on_delete=models.SET_NULL, null=True, verbose_name='触发规则')
    confirmer = models.CharField(max_length=50, null=True, blank=True, verbose_name='确认人')
    confirm_time = models.DateTimeField(null=True, blank=True, verbose_name='确认时间')
    resolver = models.CharField(max_length=50, null=True, blank=True, verbose_name='解决人')
    resolve_time = models.DateTimeField(null=True, blank=True, verbose_name='解决时间')
    comment = models.TextField(null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'monitor_alert_history'
        verbose_name = '告警历史'
        verbose_name_plural = verbose_name
        ordering = ['-alert_time']