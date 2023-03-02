from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User


@login_required
def search(request):
    context = {}
    url_parameter = request.GET.get("q")

    if url_parameter:
        users = User.objects.filter(username__icontains=url_parameter)
    else:
        users = []

    context["users"] = users

    is_ajax_request = (request.headers.get("x-requested-with")
                       == "XMLHttpRequest")

    if is_ajax_request:
        html = render_to_string(
            template_name="accounts/search-results-partial.html",
            context=context
        )
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'accounts/search.html', context)
