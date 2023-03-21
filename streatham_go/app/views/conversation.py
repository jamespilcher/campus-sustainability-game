from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def conversation(request):
    # the conversation javascript has context variables
    # that need to be rendered

    # render the conversation javascript
    return render(request, 'app/conversation.js',
                  content_type='text/javascript')
