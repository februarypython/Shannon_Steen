from django.shortcuts import render, redirect
from .models import League, Team, Player

from . import team_maker

def index(request):
	context = {
		"baseball": League.objects.filter(sport="Baseball"),
		"womens": League.objects.filter(name__contains="Womens"),
		"hockey": League.objects.filter(sport__contains="Hockey"),
		"no_football": League.objects.exclude(sport="Football"),
		"conference": League.objects.filter(name__contains="conference"),
		"atlantic":League.objects.filter(name__contains="Atlantic"),
		"dallas": Team.objects.filter(location="Dallas"),
		"raptors": Team.objects.filter(team_name__contains="Raptors"),
		"city": Team.objects.filter(location__contains="City"),
		"t_begins": Team.objects.filter(team_name__startswith="T"),
		"alpha_loc": Team.objects.order_by("location"),
		"desc_name": Team.objects.order_by("-team_name"),
		"cooper": Player.objects.filter(last_name="Cooper"),
		"joshua": Player.objects.filter(first_name="Joshua"),
		"cooper_nojosh": Player.objects.filter(last_name="Cooper").exclude(first_name="Joshua"),
		"alex_wyatt": Player.objects.filter(first_name="Alexander")|Player.objects.filter(first_name="Wyatt")
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")