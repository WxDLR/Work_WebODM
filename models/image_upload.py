from .task import Task, assets_directory_path
from django.db import models

def image_directory_path(image_upload, filename):
    return assets_directory_path(image_upload.task.id, image_upload.task.project.id, filename)


class ImageUpload(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, help_text="图片所属任务")
    image = models.ImageField(upload_to=image_directory_path, help_text="用户上传文件")

    def __str__(self):
        return self.image.name

    def path(self):
        return self.image.path
