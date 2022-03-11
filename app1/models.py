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
    description = models.TextField(max_length=512, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        """Meta definition for Group."""

        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return f'{self.name} (owner={self.owner})'



class UserJoinRecord(models.Model):
    """Model definition for UserJoinRecord."""

    user                = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_records')
    group               = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_records')
    timestamp           = models.DateTimeField(auto_now_add=True)
    invitation_status   = models.BooleanField(default=False)

    class Meta:
        """Meta definition for UserJoinRecord."""

        verbose_name = 'UserJoinRecord'
        verbose_name_plural = 'UserJoinRecords'

    def __str__(self):
        """Unicode representation of UserJoinRecord."""
        return f'{self.user} -> {self.group} [{self.invitation_status}]'


class GroupConnectionRecord(models.Model):
    """Model definition for GroupConnectionRecord."""

    from_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='from_connections', null=False)
    to_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='to_connections', null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    application_status = models.BooleanField(default=False)

    class Meta:
        """Meta definition for GroupConnectionRecord."""

        verbose_name = 'GroupConnectionRecord'
        verbose_name_plural = 'GroupConnectionRecords'

    def __str__(self):
        """Unicode representation of GroupConnectionRecord."""
        return f'{self.groups}'



class Message(models.Model):
    text = models.CharField(max_length=256, blank=False, null=False)
    
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recieved_messages")
    created_at  = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        """Meta definition for Message."""

        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        """Unicode representation of Message."""
        return f'{self.text} - {self.from_user} - {self.to_user}'