
from django.contrib.auth import models


class UserManager(models.BaseUserManager):

    def create(self, username, password, **kwargs):
        fields = {'username': username}
        fields.update(kwargs)

        user = self.model(**fields)
        user.set_password(password)
        user.save()

        return user
