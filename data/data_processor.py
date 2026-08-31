import json
import os

def search_api_data(team_name: str) -> dict:
    json_path = "dados.json" 
    
    if not os.path.exists(json_path):
        return {"status": "error", "message": "Arquivo dados.json não encontrado no diretório."}
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return {"status": "error", "message": f"Erro ao ler dados.json: {e}"}
    
    team_stats = None
    for league, teams in data.items():
        for json_team_name, t_data in teams.items():
            if json_team_name.upper() == team_name.upper():
                team_stats = t_data
                break
        if team_stats:
            break
            
    if not team_stats or team_stats.get("1_gols_pro") is None:
        return {"status": "error", "message": f"O time '{team_name}' não foi encontrado ou possui dados nulos."}
    
    try:
        num_games = team_stats["10_numero_de_jogos"]
        if not num_games or num_games == 0:
            return {"status": "error", "message": f"O time '{team_name}' não foi encontrado ou possui dados nulos."}
            
        goals_pro = team_stats["1_gols_pro"]
        goals_against = team_stats["5_gols_contra_sofridos"]
        clean_sheets = team_stats["11_jogos_sem_sofrer_gols"]
        win_percentage = team_stats["12_porcentagem_de_vitoria"]
        shtos_received = team_stats["6_chutes_sofridos"]
        shots_made = team_stats["2_chutes_feitos"]
        scoreless_games = team_stats["7_jogos_sem_fazer_gol"]
        Percentage_Home_games = team_stats["aproveitamento_casa"]
        Percentage_Away_games = team_stats["aproveitamento_fora"]
        
        
        clean_data = {
            "attack": {
                "goals_scored_per_game": float(goals_pro),
                "wins_percentage": float(win_percentage),
                "shots_made_per_game": float(shots_made),
                "scoreless_percentage": float((scoreless_games/num_games)*100),
                "Percentage of home points won": float(Percentage_Home_games/100),
                "Percentage of away points won": float(Percentage_Away_games/100),
            },
            "defense": {
                "goals_suffered_per_game": float(goals_against),
                "clean_sheets_percentage": float((clean_sheets / num_games) * 100),
                "shots_suffered_per_game": float(shtos_received)
            }
        }
        return clean_data
        
    except (KeyError, TypeError, ZeroDivisionError) as e:
        return {"status": "error", "message": f"Erro ao processar as estatísticas do time: {e}"}
