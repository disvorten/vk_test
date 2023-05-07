from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    friends = models.ManyToManyField('User', blank=True)

    def __str__(self):
        return ' '.join([
            self.first_name,
            self.last_name,
        ])


class Friend_Request(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return ' '.join([str(self.from_user), str(self.to_user)])

    def to_us(self):
        return self.to_user

    def from_us(self):
        return self.from_user
