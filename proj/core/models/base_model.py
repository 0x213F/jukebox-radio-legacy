
from django.db import models


class BaseModel(models.Model):

    class Meta:
        abstract = True

    def _assert_attribute_not_in_kwargs(self, attribute, kwargs):
        try:
            kwargs.get(attribute)
            raise ValueError(
                f'{self.__name__}.{attribute} should not be in **kwargs.'
            )
        except AttributeError:
            pass

    def _set_default_attribute(self, attribute, expected, **data):
        try:
            field_val = data.get(attribute)
            if field_val not in expected:
                expected_str = ', '.join(f'`{expected}`')
                raise ValueError(
                    f'{self.__name__}.{attribute} needs to be one of the '
                    f'following: {expected_str}.'
                )
        except AttributeError:
            data[attribute] = expected
        return data
