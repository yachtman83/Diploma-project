from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.user.username} at {self.created_at}"

# Create your models here.
