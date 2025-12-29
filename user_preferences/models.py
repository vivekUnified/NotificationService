from django.db import models

class UserPreference(models.Model):
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('slack', 'Slack'),
        ('in_app', 'In-App'),
        ('teams', 'Teams'),
    ]

    user_id = models.CharField(max_length=100)
    channel = models.CharField(max_length=50, choices=CHANNEL_CHOICES)
    enabled = models.BooleanField(default=True)
    destination = models.CharField(max_length=255, help_text="Email address, Webhook URL, etc.")
    
    class Meta:
        unique_together = ('user_id', 'channel')

    def __str__(self):
        return f"{self.user_id} - {self.channel} ({'On' if self.enabled else 'Off'})"
