import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone
from guardian.models import GroupObjectPermissionBase
from guardian.models import UserObjectPermissionBase
from guardian.shortcuts import get_perms_for_model, assign_perm

from app import pending_actions

from nodeodm import status_codes

logger = logging.getLogger('app.logger')


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, help_text="项目创建者")
    name = models.CharField(max_length=255, help_text="项目概要")
    description = models.TextField(default="", blank=True, help_text="项目介绍")
    created_at = models.DateTimeField(default=timezone.now, help_text="创建时间")
    deleting = models.BooleanField(db_index=True, default=False, help_text="无论此项目是否被标记为删除。正在执行任务的项目需等待其任务执行完毕之后方可删除！")

    def delete(self, *args):
        # No tasks?
        if self.task_set.count() == 0:
            # Just delete normally
            logger.info("Deleted project {}".format(self.id))
            super().delete(*args)
        else:
            # Need to remove all tasks before we can remove this project
            # which will be deleted by workers after pending actions
            # have been completed
            self.task_set.update(pending_action=pending_actions.REMOVE)
            self.deleting = True
            self.save()
            logger.info("Tasks pending, set project {} deleting flag".format(self.id))

    def __str__(self):
        return self.name

    def tasks(self):
        return self.task_set.only('id')

    def get_map_items(self):
        return [task.get_map_items() for task in self.task_set.filter(
                    status=status_codes.COMPLETED
                ).filter(Q(orthophoto_extent__isnull=False) | Q(dsm_extent__isnull=False) | Q(dtm_extent__isnull=False))
                .only('id', 'project_id')]

    class Meta:
        permissions = (
            ('view_project', 'Can view project'),
        )


@receiver(signals.post_save, sender=Project, dispatch_uid="project_post_save")
def project_post_save(sender, instance, created, **kwargs):
    """
    Automatically assigns all permissions to the owner. If the owner changes
    it's up to the user/developer to remove the previous owner's permissions.
    """
    for perm in get_perms_for_model(sender).all():
        assign_perm(perm.codename, instance.owner, instance)


class ProjectUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(Project, on_delete=models.CASCADE)
