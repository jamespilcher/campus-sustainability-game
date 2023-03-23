# return a list of context variables to be used in all
# templates
def messages(request):
    return {
        # used for login success
        "LOGIN_SUCCESS": "Login Successful",
        # used for login failer
        "LOGIN_FAILURE": "Incorrect Username Or Password",
        # used for inavtive user
        "LOGIN_INACTIVE": ("Your email is not verified. "
                           "Please use the verification link "
                           "sent to your email to verify"),
        # used for register success
        "REGISTER_SUCCESS": ("Account Successfully Created! Please "
                             "check your email for the activation link"),
        # used for register failure
        "REGISTER_FAILURE": "Failed To Create User. Please Try Again Later",
        # used for register email failure
        "REGISTER_EMAIL_FAILURE": ("Failed to send email, "
                                   "Maybe try a different email"),
        # used for logout success
        "LOGOUT_SUCCESS": "Logged Out! Goodbye",
    }
