def messages(request):
    return {
        "LOGIN_SUCCESS": "Login Successful",
        "LOGIN_FAILURE": "Incorrect Username Or Password",
        "REGISTER_SUCCESS": ("Account Successfully Created! Please "
                             "check your email for the activation link"),
        "REGISTER_FAILURE": "Failed To Create User. Please Try Again Later",
        "LOGOUT_SUCCESS": "Logged Out! Goodbye",
    }
