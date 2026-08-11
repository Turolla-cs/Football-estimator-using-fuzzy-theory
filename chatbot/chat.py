import os
import json

from dotenv import load_dotenv
from groq import Groq 

from data.data_processor import search_api_data
from data.fuzzy_engine import calculate_fuzzy_prediction


load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def prediction(home_team: str, away_team: str) -> str:
    """
    It uses fuzzy logic to predict dominance and the trend of the outcome and characteristics of a soccer match.
    Use this tool WHENEVER the user asks for a prediction or an analysis of a matchup between two teams.
    """
    print(f"\n[System: Gemini activated the Fuzzy engine for {home_team} vs {away_team}...]\n")
    
    home = search_api_data(home_team.upper())
    away = search_api_data(away_team.upper())

    try:
        home_data_attack = home["attack"]
        home_data_defense = home["defense"]
        away_data_attack = away["attack"]
        away_data_defense = away["defense"]
    except (KeyError, TypeError) as e:
        return f"Error processing match data structure: {e}"


    result = calculate_fuzzy_prediction(home_data_attack, home_data_defense, away_data_attack, away_data_defense)
    return f"{home_team} has a {result.output1} chance of ''Winning'' this match and {away_team} has a {result.output2} chance of ''Winning'' this match (chances measured from 0 to 10)"

tools = [
    {
        "type": "function",
        "function": {
            "name": "prediction",
            "description": "It uses fuzzy logic to predict dominance and the trend of the outcome and characteristics of a soccer match. Use this tool WHENEVER the user asks for a prediction or an analysis of a matchup between two teams.",
            "parameters": {
                "type": "object",
                "properties": {
                    "home_team": {
                        "type": "string",
                        "description": "Name of the home team (e.g., Real Madrid, Corinthians)"
                    },
                    "away_team": {
                        "type": "string",
                        "description": "Name of the away team (e.g., Barcelona, Flamengo)"
                    }
                },
                "required": ["home_team", "away_team"]
            }
        }
    }
]
system_instruction = "You are a soccer match outcome predictor and informer. Whenever the user asks for a prediction, use the provided tool to obtain the actual data calculated by the fuzzy system. Respond politely, explaining the prediction based EXCLUSIVELY on the numbers returned by the tool. Do not invent data. ONLY accepts request with teams that play in la liga or serie A or league one or premier league or bundesliga or brasileirão serie A. When someone asks for information you do NOT invent data and use your searching tools to inform about the asked team."

messages = [
    {
        "role": "system",
        "content": system_instruction
    }
]

def activate():
    print("Type 'quit' to exit the application. \n")

    while True:
        try:
            question = input("\nYou: ")
            if question.lower() == 'quit':
                print("Exiting system...")
                break

            messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages = messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                messages.append(response_message)

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if function_name == "prediction":
                        function_response = prediction(
                            home_team=function_args.get("home_team"),
                            away_team=function_args.get("away_team")
                        )

                        messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response,
                            }
                        )
                second_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.7
                )

                final_reply = second_response.choices[0].message.content
                messages.append({"role": "assistant", "content": final_reply})
                print(f"\nAssistant: {final_reply}")
            else:
                final_reply = response_message.content
                messages.append({"role": "assistant", "content": final_reply})
                print(f"\nAssistant: {final_reply}")
                
        except Exception as e:
            print(f"\n[Error]: An issue occurred: {e}")
