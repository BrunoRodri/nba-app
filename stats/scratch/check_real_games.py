from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

def check_actual_matchups():
    try:
        # Buscando jogos de Playoff da temporada 2023-24 (ou a atual do ambiente)
        # 004 é o prefixo para Playoffs
        gamefinder = leaguegamefinder.LeagueGameFinder(season_type_nullable='Playoffs')
        games = gamefinder.get_data_frames()[0]
        
        if games.empty:
            print("Nenhum jogo de playoff encontrado.")
            return

        # Filtrar apenas colunas relevantes
        games = games[['TEAM_NAME', 'MATCHUP', 'GAME_DATE', 'GAME_ID']]
        
        # O MATCHUP vem no formato "OKC vs. PHX" ou "OKC @ PHX"
        print("--- ÚLTIMOS CONFRONTOS DE PLAYOFF ENCONTRADOS ---")
        print(games.head(20))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_actual_matchups()
