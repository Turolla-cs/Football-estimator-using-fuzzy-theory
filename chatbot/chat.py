import os

from dotenv import load_dotenv
from google import genai

from data.data_processor import search_api_data
from data.fuzzy_engine import calculate_fuzzy_prediction
from data.fuzzy_engine import Result

load_dotenv()
chave = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=chave)

def prediction(home_team: str, away_team: str) -> dict:
    """
    It uses fuzzy logic to predict dominance and the trend of the outcome and characteristics of a soccer match.
    Use this tool WHENEVER the user asks for a prediction or an analysis of a matchup between two teams.
    """
    print(f"\n[System: Gemini activated the Fuzzy engine for {home_team} vs {away_team}...]\n")
    
    home_data_attack = search_api_data(home_team)
    home_data_defense = search_api_data(home_team)
    away_data_attack = search_api_data(away_team)
    away_data_defense = search_api_data(away_team)
    result = calculate_fuzzy_prediction(home_data_attack, home_data_defense, away_data_attack, away_data_defense)
    return print(f"{home_team} has a {result.output1} chance of ''Winning'' this match and {away_team} has a {result.output2} chance of ''Winning'' this match (chances measured from 0 to 10)")
    #fazer ainda tratamento de erros e colocar algum printf de loading pra não parecer que travou
    

chat = client.chats.create(
    model ="gemini-2.5-flash",
    config={
        "system_instruction": "You are a soccer match outcome predictor. Whenever the user asks for a prediction, use the provided tool to obtain the actual data calculated by the fuzzy system. Respond politely, explaining the prediction based EXCLUSIVELY on the numbers returned by the tool. Do not invent data.",
        "temperature": 0.7,
        "tools": [prediction] 
    },
)

print("Type 'quit' to end.")
while True:
    question = input("\nYou: ")
    if question.lower() == 'quit':
        break
response = chat.send_message(question)
print(f"\nAssistant: {response.text}")