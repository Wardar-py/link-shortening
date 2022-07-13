from django.db import models
from user.models import User


class Link(models.Model):
    """
    The Link model
    """
    full_link = models.TextField()
    short_link = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'ссылка'
        verbose_name_plural = 'ссылки'
        ordering = ["-created_at"]

    def __str__(self):
        return self.short_link
