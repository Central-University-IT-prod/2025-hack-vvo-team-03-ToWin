import games.models
from django.shortcuts import render
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib.auth.decorators import login_required

# Настройка схемы Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Pastebin API",
        default_version='v1',
        description="Документация API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def check_user_in_game(user, comp):
    gs = games.models.Game.objects.filter(competition=comp, player1=user)
    if gs:
        return True
    gs = games.models.Game.objects.filter(competition=comp, player2=user)
    if gs:
        return True
    return False


@login_required
def index(request):
    context = {}
    template_name = 'index.html'
    competitions = games.models.Competition.objects.all().order_by('-count_player_now')
    context['competitions'] = competitions
    context['inf_join'] = {}

    if request.user.is_authenticated:
        for c in competitions:
            context['inf_join'][c.id] = check_user_in_game(request.user, c)
    else:
        for c in competitions:
            context['inf_join'][c.id] = False

    return render(request, template_name=template_name, context=context)
