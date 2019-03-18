
import random
import string

from django.db import models


class ChessManager(models.Manager):

    @staticmethod
    def generate_code():
        from .models import Chess
        return random.sample(
            string.ascii_lowercase + string.digits,
            Chess.CODE_LENGTH
        )
