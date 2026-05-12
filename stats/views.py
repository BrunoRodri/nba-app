from django.shortcuts import render
from django.http import JsonResponse
from . import services, team_constants


def index(request):
    """Home page — hero section + all 30 NBA teams grid."""
    teams = services.search_teams('').order_by('nickname')  # returns all teams ordered by franchise name
    context = {
        'teams': teams,
        'season': services.get_current_season(),
    }
    return render(request, 'stats/index.html', context)


def search(request):
    """Global search — identifies players and teams matching the query."""
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, 'stats/search_results.html', {
            'query': '',
            'players': [],
            'teams': [],
        })

    players = services.search_players(query)
    teams = services.search_teams(query)

    # Prefer active players first
    players = players.order_by('-is_active', 'full_name')[:20]
    teams = teams[:10]

    context = {
        'query': query,
        'players': players,
        'teams': teams,
    }
    return render(request, 'stats/search_results.html', context)


def player_detail(request, player_id):
    """Player profile page — bio, career stats, recent games."""
    if not request.GET.get('fetch'):
        from django.urls import reverse
        return render(request, 'stats/loading_skeleton.html', {
            'target_url': reverse('stats:player_detail', args=[player_id]) + '?fetch=1',
            'title': 'Carregando Dados do Jogador...',
        })
        
    player_info = services.get_player_info(player_id)
    career_data = services.get_player_career_stats(player_id)
    season = services.get_current_season()
    game_log = services.get_player_game_log(player_id, season=season)

    # Add team colors for dynamic gradient
    team_abbr = player_info.get('TEAM_ABBREVIATION') if player_info else None
    team_colors = team_constants.get_team_colors(team_abbr)

    context = {
        'player': player_info,
        'career': career_data,
        'game_log': game_log,
        'season': season,
        'player_id': player_id,
        'team_colors': team_colors,
        'api_error': not player_info or not (career_data and career_data.get('career')),
    }
    return render(request, 'stats/player_detail.html', context)


def team_detail(request, team_id):
    """Team profile page — info, roster, season record, recent games."""
    if not request.GET.get('fetch'):
        from django.urls import reverse
        return render(request, 'stats/loading_skeleton.html', {
            'target_url': reverse('stats:team_detail', args=[team_id]) + '?fetch=1',
            'title': 'Carregando Dados da Franquia...',
        })
        
    team_info = services.get_team_info(team_id)
    season = services.get_current_season()
    roster = services.get_team_roster(team_id, season=season)
    record = services.get_team_season_record(team_id, season=season)
    history = services.get_team_history(team_id)
    
    # Add team colors for dynamic gradient
    team_abbr = team_info.get('ABBREVIATION') if team_info else None
    team_colors = team_constants.get_team_colors(team_abbr)

    context = {
        'team': team_info,
        'roster': roster,
        'record': record,
        'history': history,
        'season': season,
        'team_id': team_id,
        'team_colors': team_colors,
        'api_error': not team_info or not roster or not history or not (record and record.get('games')),
    }
    return render(request, 'stats/team_detail.html', context)

def team_season_games(request, team_id, season):
    """View to show all games for a specific team in a specific season."""
    if not request.GET.get('fetch'):
        from django.urls import reverse
        return render(request, 'stats/loading_skeleton.html', {
            'target_url': reverse('stats:team_season_games', args=[team_id, season]) + '?fetch=1',
            'title': f'Carregando Jogos da Temporada {season}...',
        })
        
    team_info = services.get_team_info(team_id)
    games = services.get_team_season_games(team_id, season)

    context = {
        'team': team_info,
        'games': games,
        'season': season,
        'team_id': team_id,
    }
    return render(request, 'stats/team_season_games.html', context)

def game_detail(request, game_id):
    """Game detail page — full boxscore."""
    if not request.GET.get('fetch'):
        from django.urls import reverse
        return render(request, 'stats/loading_skeleton.html', {
            'target_url': reverse('stats:game_detail', args=[game_id]) + '?fetch=1',
            'title': 'Carregando Box Score da Partida...',
        })
        
    boxscore = services.get_game_boxscore(game_id)

    if not boxscore:
        from django.shortcuts import redirect
        return redirect('stats:index')

    context = {
        'game_id': game_id,
        'boxscore': boxscore,
    }
    return render(request, 'stats/game_detail.html', context)


def search_api(request):
    """API endpoint for search autocomplete."""
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'players': [], 'teams': []})

    players = services.search_players(query).order_by('-is_active', 'full_name')[:5]
    teams = services.search_teams(query).order_by('nickname')[:5]

    return JsonResponse({
        'players': [{
            'id': p.nba_id, 
            'name': p.full_name, 
            'is_active': p.is_active,
            'url': f'/player/{p.nba_id}/'
        } for p in players],
        'teams': [{
            'id': t.nba_id, 
            'name': t.full_name, 
            'city': t.city,
            'url': f'/team/{t.nba_id}/'
        } for t in teams],
    })
