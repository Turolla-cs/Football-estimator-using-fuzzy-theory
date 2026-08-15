import os
import json
from dotenv import load_dotenv
from groq import Groq 
from data.data_processor import search_api_data
from data.fuzzy_engine import calculate_fuzzy_prediction

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

system_instruction = "You are a soccer match outcome predictor and informer. Whenever the user asks for a prediction, use the provided tool to obtain the actual data calculated by the fuzzy system. Respond politely, explaining the prediction based EXCLUSIVELY on the numbers returned by the tool. Do not invent data."

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
    return f"{home_team} has a {result.output1:.2f} chance of winning and {away_team} has a {result.output2:.2f} chance of winning."

def process_chat_message(messages: list, question: str) -> str:
    messages.append({"role": "user", "content": question})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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
            model="llama-3.3-70b-versatile",
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