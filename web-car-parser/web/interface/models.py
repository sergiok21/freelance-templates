from django.db import models


class User(models.Model):
    t_id = models.PositiveBigIntegerField(unique=True, default=0)
    token = models.UUIDField(unique=True, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Telegram ID: {self.t_id} | Admin: {self.is_superuser}'


class Filter(models.Model):
    user = models.ForeignKey(to=User, related_name='filters', on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    link = models.TextField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Filter'
        verbose_name_plural = 'Filters'
        ordering = ['id']

    def __str__(self):
        return f'Name: {self.name} | User: {self.user.t_id} | Status: {self.status}'
