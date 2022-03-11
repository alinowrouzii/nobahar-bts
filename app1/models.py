from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # email = models.CharField(unique=True,blank=False, null=False ,max_length=50)
    name = models.CharField(max_length=50, default="")
    def __str__(self):
        return f"{self.email} - {self.name}"


class Group(models.Model):

    owner       = models.OneToOneField(User, on_delete=models.CASCADE)
    name        = models.CharField(max_length=128, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Meta definition for Group."""

        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return f'{self.name} (owner={self.owner})'



class UserJoinRecord(models.Model):
    """Model definition for UserJoinRecord."""

    user                = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    group               = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='records')
    timestamp           = models.DateTimeField(auto_now_add=True)
    invitation_status   = models.BooleanField(default=False)

    class Meta:
        """Meta definition for UserJoinRecord."""

        verbose_name = 'UserJoinRecord'
        verbose_name_plural = 'UserJoinRecords'

    def __str__(self):
        """Unicode representation of UserJoinRecord."""
        return f'{self.user} -> {self.group} [{self.invitation_status}]'
