from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def length_validator(value):
    if value is not None:
        if value not in range(99999, 999999):
            raise ValidationError(
                _('Value must be 6 digit number'),
                params={'value': value},
            )