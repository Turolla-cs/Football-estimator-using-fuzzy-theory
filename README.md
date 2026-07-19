# Football-Match-Predictor-using-fuzzy-theory

* A Python-based AI tool that uses Fuzzy Logic and real-time football statistics to predict match outcomes. This project integrates the Google Gemini API for natural language processing and the API-Football service for live game data 
    * (The free tier only has access to the 2024 season as the latest. If you wish to use newer seasons, please switch to another plan and change the season parameter in data_processor.py from 2024 to your target season.)

## Features
- **Fuzzy Logic Engine:** Calculates offensive and defensive dominance using scikit-fuzzy.
- **AI-Powered Interface:** Chat with the assistant to get match predictions.
- **Efficient Caching:** Built-in daily cache system to optimize API usage.

## Prerequisites
- Python 3.10+
- An API key from [API-Football](https://www.api-football.com/)
- An API key from [Google AI Studio](https://aistudio.google.com/)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-folder>
2. Create a virtual enviroment (using package manager uv):
   *  `uv` creates the environment inside a directory named `.venv` by default, which is the standard convention for Python projects.
3. Install dependencies:
    * uv add requests python-dotenv google-genai numpy scikit-fuzzy scipy packaging networkx
4. Configure your environment variables:
    * Create a file named .env in the root folder.
    * Add your keys:
        FOOTBALL_API_KEY=your_api_football_key
        GEMINI_API_KEY=your_gemini_key
5. Usage:
    * uv run main.py

## Project Structure:
    * main.py: Entry point of the application.

    * chat.py: Handles Gemini chat interactions and tool calling.

    * data/data_processor.py: Manages API communication and caching.

    * data/fuzzy_engine.py: Contains the mathematical logic for predictions.