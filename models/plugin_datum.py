import logging
from django.db import models
from django.contrib.postgres import fields
from django.contrib.auth.models import User

logger = logging.getLogger('app.logger')

class PluginDatum(models.Model):
    key = models.CharField(max_length=255, help_text="关键字设置", db_index=True)
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, help_text="用户所属设置，若为空，则默认为全局设置")
    int_value = models.IntegerField(blank=True, null=True, default=None, help_text="整数值")
    float_value = models.FloatField(blank=True, null=True, default=None, help_text="浮点数值")
    bool_value = models.NullBooleanField(blank=True, null=True, default=None, help_text="布尔值")
    string_value = models.TextField(blank=True, null=True, default=None, help_text="字符串")
    json_value = fields.JSONField(default=None, blank=True, null=True, help_text="JSON")

    def __str__(self):
        return self.key
