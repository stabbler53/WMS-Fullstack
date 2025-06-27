# audit/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import AuditLog

User = get_user_model()

@receiver(post_save, sender=User)
def log_user_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    AuditLog.objects.create(
        user=instance,
        action=f"User {action}",
        object_repr=str(instance)
    )

@receiver(post_delete, sender=User)
def log_user_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=instance,
        action="User deleted",
        object_repr=str(instance)
    )
