from django.db import models
from django.contrib.auth import get_user_model


class Environment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    env_name = models.CharField(max_length=100)
    config = models.JSONField()

    def __str__(self):
        return self.env_name
