def messages(request):
    return {
        "LOGIN_SUCCESS": "Login Successful",
        "LOGIN_FAILURE": "Incorrect Username Or Password",
        "LOGIN_INACTIVE": ("Your email is not verified. "
                           "Please use the verification link "
                           "sent to your email to verify"),
        "REGISTER_SUCCESS": ("Account Successfully Created! Please "
                             "check your email for the activation link"),
        "REGISTER_FAILURE": "Failed To Create User. Please Try Again Later",
        "REGISTER_EMAIL_FAILURE": ("Failed to send email, "
                                   "Maybe try a different email"),
        "LOGOUT_SUCCESS": "Logged Out! Goodbye",
    }
