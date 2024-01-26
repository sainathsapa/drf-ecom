from django.db import models

import binascii
import os
from customer.models import Customer


class UserAuthTokenModel(models.Model):
    """
    The default authorization token model.
    """

    key = models.CharField("Key", max_length=40, primary_key=True)

    customer = models.OneToOneField(
        Customer,
        related_name="auth_token",
        on_delete=models.CASCADE,
        verbose_name="Customer",
    )
    created = models.DateTimeField(("Created"), auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(UserAuthTokenModel, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
