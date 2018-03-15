# Simple finds

Question | Expected Output
--- | ---
1. Find all baseball leagues | International Collegiate Baseball Conference, Atlantic Federation of Amateur Baseball Players
    League.objects.filter(sport="Baseball")
    
2. Find all womens' leagues | International Association of Womens' Basketball Players, Transamerican Womens' Football Athletics Conference
    League.objects.filter(name__contains="Womens")

3. Find all leagues where sport is any type of hockey | International Conference of Amateur Ice Hockey, Atlantic Amateur Field Hockey League, Pacific Ice Hockey Conference
    League.objects.filter(sport__contains="Hockey")

4. Find all leagues where sport is something OTHER THAN football | International Conference of Amateur Ice Hockey, International Collegiate Baseball Conference, Atlantic Federation of Amateur Baseball Players, Atlantic Federation of Basketball Athletics, Atlantic Soccer Conference, International Association of Womens' Basketball Players, Atlantic Amateur Field Hockey League, Pacific Ice Hockey Conference
    League.objects.exclude(sport="Football")

5. Find all leagues that call themselves "conferences" | International Conference of Amateur Ice Hockey, International Collegiate Baseball Conference, Atlantic Soccer Conference, American Conference of Amateur Football, Transamerican Womens' Football Athletics Conference, Pacific Ice Hockey Conference
    League.objects.filter(name__contains="conference")
    
6. Find all leagues in the Atlantic region | Atlantic Federation of Amateur Baseball Players, Atlantic Federation of Basketball Athletics, Atlantic Soccer Conference, Atlantic Amateur Field Hockey League
    League.objects.filter(name__contains="Atlantic")

7. Find all teams based in Dallas | Dallas Nets, Dallas Angels
    Team.objects.filter(location="Dallas")

8. Find all teams named the Raptors | Atlanta Raptors, Golden State Raptors
    Team.objects.filter(team_name__contains="Raptors")

9. Find all teams whose location includes "City" | Mexico City Cave Spiders, Kansas City Spurs
    Team.objects.filter(location__contains="City")

10. Find all teams whose names begin with "T" | Alberta Texans, Michigan Timberwolves, Manitoba Tiger-Cats, Colorado Twins
    Team.objects.filter(team_name__startswith="T")

11. Return all teams, ordered alphabetically by location | *too many to list*
    Team.objects.order_by("location")

12. Return all teams, ordered by team name in reverse alphabetical order | *too many to list*
    Team.objects.order_by("-team_name")

13. Find every player with last name "Cooper" | Joshua Cooper, Landon Cooper, Michael Cooper, Alexander Cooper
    Player.objects.filter(last_name="Cooper")

14. Find every player with first name "Joshua" | Joshua Cooper, Joshua Hayes, Joshua Henderson, Joshua Long, Joshua Coleman, Joshua White, Joshua Parker, Joshua Smith
    Player.objects.filter(first_name="Joshua")

15. Find every player with last name "Cooper" EXCEPT FOR Joshua | Landon Cooper, Michael Cooper, Alexander Cooper
    Player.objects.filter(last_name="Cooper").exclude(first_name="Joshua")

16. Find all players with first name "Alexander" OR first name "Wyatt" | Wyatt Bell, Alexander Bailey, Wyatt Peterson, Alexander Wright, Wyatt Alexander, Wyatt Bennett, Alexander Parker, Alexander Adams, Alexander Walker, Alexander Flores, Alexander Cooper
    Player.objects.filter(first_name="Alexander")|Player.objects.filter(first_name="Wyatt")