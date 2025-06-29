from django.db import models
import uuid

class User(models.Model):
    PLAN_CHOICES = [
        ('HOBBY', 'Hobby'),
        ('PRO', 'Pro'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='HOBBY')

    def __str__(self):
        return self.name

class App(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='apps', on_delete=models.CASCADE)
    appId = models.CharField(
        max_length=40, 
        unique=True, 
        editable=False, 
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.appId:
            # Generate a unique appId: e.g., app_a1b2c3d4
            self.appId = f'app_{uuid.uuid4().hex[:8]}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
