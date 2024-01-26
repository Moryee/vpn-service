from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Site(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    visiting_count = models.BigIntegerField(default=0)
    data_volume = models.BigIntegerField(default=0)
