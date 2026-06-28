from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ticket(models.Model):
    PRIORITY_CHOICES=[
        ('P1','P1- Critical'),
        ('P2','P2- High'),
        ('P3','P3- Medium'),
    ]
    STATUS_CHOICES=[
        ('Open', 'Open'),
        ('in_progress','In Progress'),
        ('resolved','Resolved'),
    ]

    title       = models.CharField(max_length=200)
    description = models.TextField()
    priority    = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default='P3')
    status      = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    ai_suggestion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"[{self.priority}] {self.title}"
