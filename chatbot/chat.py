import os

from dotenv import load_dotenv
from google import genai

from data.data_processor import search_api_data
from data.fuzzy_engine import calculate_fuzzy_prediction


load_dotenv()
key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=key)

def prediction(home_team: str, away_team: str) -> str:
    """
    It uses fuzzy logic to predict dominance and the trend of the outcome and characteristics of a soccer match.
    Use this tool WHENEVER the user asks for a prediction or an analysis of a matchup between two teams.
    """
    print(f"\n[System: Gemini activated the Fuzzy engine for {home_team} vs {away_team}...]\n")
    
    home = search_api_data(home_team.upper())
    home_data_attack = home["attack"]
    home_data_defense = home["defense"]
    away = search_api_data(away_team.upper())
    away_data_attack = away["attack"]
    away_data_defense = away["defense"]
    result = calculate_fuzzy_prediction(home_data_attack, home_data_defense, away_data_attack, away_data_defense)
    return f"{home_team} has a {result.output1} chance of ''Winning'' this match and {away_team} has a {result.output2} chance of ''Winning'' this match (chances measured from 0 to 10)"
    #fazer ainda tratamento de erros e colocar algum printf de loading pra não parecer que travou
    

chat = client.chats.create(
    model ="gemini-2.5-flash",
    config={
        "system_instruction": "You are a soccer match outcome predictor. Whenever the user asks for a prediction, use the provided tool to obtain the actual data calculated by the fuzzy system. Respond politely, explaining the prediction based EXCLUSIVELY on the numbers returned by the tool. Do not invent data. ONLY accepts request with teams that play in la liga or serie A or league one or premier league or bundesliga or brasileirão serie A",
        "temperature": 0.7,
        "tools": [prediction] 
    },
)


def activate():
    print("Type 'quit' to exit the application.")
    while True:
        try:
            question = input("\nYou: ")
            if question.lower() == 'quit':
                print("Exiting system...")
                break
            
            response = chat.send_message(question)
            print(f"\nAssistant: {response.text}")
        except Exception as e:
            print(f"\n[Error]: An issue occurred: {e}")