from django.contrib.auth.tokens import PasswordResetTokenGenerator



class UserverificationTokenGen(PasswordResetTokenGenerator):
    def _make_token_with_timestamp(self, user, timestamp):
        return super()._make_token_with_timestamp(user, timestamp)
    


account_activation_token = UserverificationTokenGen()