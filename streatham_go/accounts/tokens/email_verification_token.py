from django.contrib.auth.tokens import PasswordResetTokenGenerator


# this class is used to generate the email verification token
class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    # this function is used to generate the hash value
    def _make_hash_value(self, user, timestamp):
        # encode the user id, username, is_active, and timestamp
        # this makes the token invalid once the user is activated
        return (
            str(user.pk) + str(user.username) +
            str(user.is_active) + str(timestamp)
        )


# create an instance of the EmailVerificationTokenGenerator class
email_verification_token = EmailVerificationTokenGenerator()
