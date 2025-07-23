from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from storages.backends.s3boto3 import S3Boto3Storage

class Journal(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_journals')
    created_at = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Entry(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.FileField(upload_to='media/%Y/%m/%d/', storage=S3Boto3Storage(), blank=True, null=True)


    def __str__(self):
        return f"Entry in {self.journal.title} at {self.created_at}"

class Permission(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)  # True for edit, False for read-only

    class Meta:
        unique_together = ('journal', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.journal.title} ({'edit' if self.can_edit else 'read'})"


