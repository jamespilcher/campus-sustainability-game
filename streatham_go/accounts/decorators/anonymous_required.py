from django.shortcuts import redirect


def anonymous_required(function=None, redirect_url='app:home'):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary by default.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator
