from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Count


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

def get_more(request):
	context = {
		"asc_teams": Team.objects.filter(league__name="Atlantic Soccer Conference"),
		"penguins_players": Player.objects.filter(curr_team__team_name="Penguins"),
		"icbc_players": Player.objects.filter(curr_team__league__name="International Collegiate Baseball Conference").all(),
		"acaf_lopez": Player.objects.filter(curr_team__league__name="American Conference of Amateur Football").filter(last_name="Lopez"),
		"football_players": Player.objects.filter(curr_team__league__sport="Football"),
		"teams_sophia": Team.objects.filter(curr_players__first_name="Sophia"),
		"leagues_sophia": League.objects.filter(teams__curr_players__first_name="Sophia"),
		"flores_not_roughriders": Player.objects.exclude(curr_team__team_name="Roughriders").filter(last_name="Flores"),
		"sam_evans": Team.objects.filter(all_players__first_name="Samuel", all_players__last_name="Evans"),
		"tiger_cats": Player.objects.filter(all_teams__team_name="Tiger-Cats"),
		"wichita_past": Player.objects.filter(all_teams__team_name="Vikings").exclude(curr_team__team_name="Vikings"),
		"jacob_gray": Team.objects.filter(all_players__first_name="Jacob", all_players__last_name="Gray").exclude(curr_players__first_name="Jacob", curr_players__last_name="Gray"),
		"afabp_joshua": Player.objects.filter(all_teams__league__name="Atlantic Federation of Amateur Baseball Players").filter(first_name="Joshua"),
		"players12": Team.objects.annotate(num_players=Count('all_players')).filter(num_players__gte=12),
		"players_by_team_count": Player.objects.annotate(num_teams=Count('all_teams')).order_by('num_teams')
	}
	return render(request, "leagues/more.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)
	return redirect("index")