import logging

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
from .task import validate_task_options

logger = logging.getLogger('app.logger')


class Preset(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, help_text="预设值所属用户")
    name = models.CharField(max_length=255, blank=False, null=False, help_text="描述预设值的标签")
    options = JSONField(default=list(), blank=True, help_text="定义预设值得选项（同Task定义项目）",
                               validators=[validate_task_options])
    created_at = models.DateTimeField(default=timezone.now, help_text="创建时间")
    system = models.BooleanField(db_index=True, default=False, help_text="不管该预设值是对所有用户有效还是只对拥有者有效")

    def __str__(self):
        return self.name
