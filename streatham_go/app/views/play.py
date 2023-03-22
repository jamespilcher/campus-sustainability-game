from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from ..models import Location, Word
from ..tokens import validate_game_jwt


# add the login required decorator
@login_required
def play(request, token):
    # initalize the context variable
    context = {}

    # get the words data

    word_data = Word.objects.all()

    words = Word.get_words(word_data)

    # get the building name from the token
    buildingName = validate_game_jwt(request, token)
    # validate the token
    if buildingName is None:
        # if the toekn is invalid, set the error message
        context['error'] = "Invalid token"
    else:
        # get the building from the database
        building = Location.objects.filter(name=buildingName).first()
        # get the game data from the building
        game_data = render_to_string('app/' + building.game.file)

        # set the context variables
        context['building_name'] = buildingName
        context['game_content'] = game_data
        context['words'] = words

    # render the play page
    return render(request, 'app/play.html', context)


@login_required
def play_js(request):
    return render(request, 'app/play.js',
                  content_type='application/javascript')
