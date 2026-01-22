from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

""" why does it not work
class UserverificationTokenGen(PasswordResetTokenGenerator):
    def _make_token_with_timestamp(self, user, timestamp):
        return super()._make_token_with_timestamp(user, timestamp)
    
"""
class UserverificationTokenGen(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = UserverificationTokenGen()