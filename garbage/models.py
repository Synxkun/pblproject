from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('active', 'Active'),
    ('removed', 'Removed'),
)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    image = models.ImageField(upload_to='reports/')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)  # To track if user notified of removal

    def __str__(self):
        return f"Report #{self.id} by {self.user.username} - {self.status}"
