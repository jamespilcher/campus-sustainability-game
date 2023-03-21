from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User


# add the login required decoratorn
@login_required
# search view function
def search(request):
    # initialize the context variable
    context = {}
    # get the search parameter from the url
    url_parameter = request.GET.get("q")

    # check if the search parameter exists
    if url_parameter:
        # if the search parameter exists, filter the users
        users = User.objects.filter(username__icontains=url_parameter)
    else:
        # if the search parameter does not exist, set the 
        # users to an empty list
        users = []

    # set the context variables
    context["users"] = users

    # check if the request is an ajax request
    is_ajax_request = (request.headers.get("x-requested-with")
                       == "XMLHttpRequest")

    # check if the request is an ajax request
    if is_ajax_request:
        # if the request is an ajax request, render the search results
        html = render_to_string(
            template_name="accounts/search-results-partial.html",
            context=context
        )
        # return the html as a json response
        data_dict = {"html_from_view": html}

        # return the data as a json response
        return JsonResponse(data=data_dict, safe=False)

    # render the search page
    return render(request, 'accounts/search.html', context)
