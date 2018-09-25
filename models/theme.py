import logging
import os
from pathlib import Path

from django.db.models import signals
from django.db import models
from colorfield.fields import ColorField
from django.dispatch import receiver

from webodm import settings

logger = logging.getLogger('app.logger')

class Theme(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False, help_text="主题名称", verbose_name='名称')

    # Similar to how discourse.org does it
    primary = ColorField(default='#2c3e50', help_text="大部分文本，图标及边框", verbose_name='基本主题')
    secondary = ColorField(default='#ffffff', help_text="主题背景颜色及部分按钮颜色", verbose_name='次级主题')
    tertiary = ColorField(default='#18bc9c', help_text="导航栏颜色", verbose_name='三级主题')

    button_primary = ColorField(default='#2c3e50', help_text="主要按钮颜色", verbose_name='基础按钮')
    button_default = ColorField(default='#95a5a6', help_text="默认按钮颜色", verbose_name='默认按钮')
    button_danger = ColorField(default='#e74c3c', help_text="删除按钮颜色", verbose_name='警告按钮')

    header_background = ColorField(default='#18bc9c', help_text="页面标题颜色", verbose_name='头部背景颜色')
    header_primary = ColorField(default='#ffffff', help_text="页面标题文字及按钮颜色", verbose_name='头部主题颜色')

    border = ColorField(default='#e7e7e7', help_text="主要边界颜色", verbose_name='边框颜色')
    highlight = ColorField(default='#f7f7f7', help_text="部分边界及面板背景颜色", verbose_name='高亮颜色')

    dialog_warning = ColorField(default='#f39c12', help_text="警告框边界颜色", verbose_name='警告框边框颜色')

    failed = ColorField(default='#ffcbcb', help_text="通知背景颜色-失败", verbose_name='失败框')
    success = ColorField(default='#cbffcd', help_text="通知背景颜色-成功", verbose_name='成功框')

    css = models.TextField(default='', blank=True, verbose_name="样式")
    html_before_header = models.TextField(default='', blank=True, verbose_name="HTML头部前")
    html_after_header = models.TextField(default='', blank=True, verbose_name="HTML头部后")
    html_after_body = models.TextField(default='', blank=True, verbose_name="HTML主体")
    html_footer = models.TextField(default='', blank=True, verbose_name="HTML尾部")

    def __str__(self):
        return self.name


@receiver(signals.post_save, sender=Theme, dispatch_uid="theme_post_save")
def theme_post_save(sender, instance, created, **kwargs):
    update_theme_css()


def update_theme_css():
    """
    Touch theme.scss to invalidate its cache and force
    compressor to regenerate it
    """

    theme_file = os.path.join('app', 'static', 'app', 'css', 'theme.scss')
    try:
        Path(theme_file).touch()
        logger.info("刷新{}缓存".format(theme_file))
    except:
        logger.warning("无法访问{}".format(theme_file))
