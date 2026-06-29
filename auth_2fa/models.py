from django.db import models
from django.conf import settings

from users.models import User


class EmailVerificationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    using_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Код    {self.verification_code} для {self.user.email}"

