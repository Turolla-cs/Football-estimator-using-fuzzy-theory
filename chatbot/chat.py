import os
import json
from dotenv import load_dotenv
from groq import Groq 
from data.data_processor import search_api_data
from data.fuzzy_engine import calculate_fuzzy_prediction

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_instruction = (
    "You are a soccer match outcome predictor and informer. "
    "Whenever the user asks for a prediction, use the provided tool to obtain the actual data calculated by the fuzzy system. "
    "Respond politely, explaining the prediction based EXCLUSIVELY on the numbers returned by the tool. Do not invent data. "
    "ONLY accept requests with teams that play in La Liga or Segunda división, Serie A or B, League One or Two, Premier League or championship, Bundesliga or Bundesliga 2, or Brasileirão Série A or Série B. "
    "When providing match predictions, you must format the response using Markdown: use a short introductory sentence, then a bullet list (lines starting with '- ') for each stat, team, or topic, so the content displays cleanly as bulletpoints on the frontend. Use **bold** only for key numbers or team names. Avoid large blocks of plain text. "
    "At the very end of any response containing historical information or external data, always include the source (font) of your search."
    "When presenting a match prediction, only state the percentage/advantage of the favored team returned by the tool. Never mention, calculate, or imply the percentage of the team with less advantage."
    "Adjust how you phrase that percentage based on its value: if it is below 5%, tell the user the match trends toward a draw and do not name a favorite; if it is 5% or higher and up to 100%, name the favored team and state the percentage, wording the confidence level in proportion to the number (a slight edge near 5%, a heavy favorite as it nears 100%); if it exceeds 100%, do not display the raw number at all — instead tell the user the favored team is an overwhelming favorite in this matchup."
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "prediction",
            "description": "It uses fuzzy logic to predict dominance and the trend of the outcome of a soccer match.",
            "parameters": {
                "type": "object",
                "properties": {
                    "home_team": {"type": "string", "description": "Name of the home team"},
                    "away_team": {"type": "string", "description": "Name of the away team"}
                },
                "required": ["home_team", "away_team"]
            }
        }
    }
]

def prediction(home_team: str, away_team: str) -> str:
    home = search_api_data(home_team)
    away = search_api_data(away_team)

    if home.get("status") == "error":
        return f"Error retrieving data for {home_team}: {home.get('mensage')}"
            
    if away.get("status") == "error":
        return f"Error retrieving data for {away_team}: {away.get('mensage')}"

    result = calculate_fuzzy_prediction(home["attack"], home["defense"], away["attack"], away["defense"])
    if result.output1 >= result.output2:
        tendencia = (result.output1 - result.output2)*100
        return f"{home_team} has a {tendencia:.2f}% advantage over {away_team}."
    if result.output2 >= result.output1:
        tendencia = (result.output2 - result.output1)*100
        return f"{away_team} has a {tendencia:.2f}% advantage over {home_team}."

def process_chat_message(messages: list, question: str) -> str:
    messages.append({"role": "user", "content": question})
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.7
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        messages.append(response_message)
        for tool_call in tool_calls:
            if tool_call.function.name == "prediction":
                args = json.loads(tool_call.function.arguments)
                func_response = prediction(args.get("home_team"), args.get("away_team"))
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": func_response,
                })
        
        second_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=0.7
        )
        final_reply = second_response.choices[0].message.content
        messages.append({"role": "assistant", "content": final_reply})
        return final_reply
    else:
        final_reply = response_message.content
        messages.append({"role": "assistant", "content": final_reply})
        return final_reply
