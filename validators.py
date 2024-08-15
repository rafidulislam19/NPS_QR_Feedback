from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r'(.*[A-Z].*){2,}', password):
            raise ValidationError(
                _("The password must contain at least two uppercase letters."),
                code='password_no_uppercase',
            )
        if not re.search(r'(.*[a-z].*){2,}', password):
            raise ValidationError(
                _("The password must contain at least two lowercase letters."),
                code='password_no_lowercase',
            )
        if not re.search(r'(.*\d.*){2,}', password):
            raise ValidationError(
                _("The password must contain at least two numerical digits."),
                code='password_no_number',
            )
        if not re.search(r'(.*\W.*){2,}', password):
            raise ValidationError(
                _("The password must contain at least two special characters."),
                code='password_no_special',
            )
    def get_help_text(self):
        return _(
            "Your password must contain at least two uppercase letters, "
            "two lowercase letters, two numerical digits, and two special characters."
        )

class NotSameAsOldValidator:
    def validate(self, password, user=None):
        if user and user.check_password(password):
            raise ValidationError(
                _("Your new password cannot be the same as the old password."),
                code='password_no_change',
            )

    def get_help_text(self):
        return _("Your new password cannot be the same as the old password.")