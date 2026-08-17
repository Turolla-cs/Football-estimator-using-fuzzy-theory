# Football Match Predictor Using Fuzzy Theory

A Python-based AI tool that leverages Fuzzy Logic and real-time football statistics to predict match outcomes. This project integrates the Groq API for natural language processing and uses FastAPI to connect the frontend with local data stored in `dados.json`.

**Data Coverage:** The dataset is updated with the complete 2025/2026 season for the top 5 European leagues and the first 22 rounds of the Brazilian top flight (Brasileirão Série A).
    The teams that were promoted to the top divisions in Europe will have their good statistics reduced by 35% and their bad statistics incremented 35%.
    If you want to know or change how the teams are being called just look their name on `dados.json` and the same if you want to update the data.

## Features
* **Fuzzy Logic Engine:** Calculates offensive and defensive dominance using `scikit-fuzzy`.
* **AI-Powered Interface:** Chat with the assistant to get match predictions.

## Prerequisites
* Python 3.10+
* FastAPI
* [uv package manager](https://docs.astral.sh/uv/) installed
* An API key from [Groq Console](https://console.groq.com/)

## Installation

    1. Clone the repository and navigate to the project folder:
        ```bash
        git clone <repository-url>
        cd <project-folder>

    2. Install dependencies and create the virtual environment (.venv) automatically:
    uv sync

    3.Configure your environment variables by creating a .env file in the root folder and copying the contents from .env.example.

## Usage

    1. Start the frontend using your preferred method (e.g., VS Code Live Server).

    2. Initialize the FastAPI backend server:
    Bash
        uv run fastapi dev back.py

    3. Open your browser and interact with the AI directly through the frontend interface.

## Project Structure

    back.py: The FastAPI server initialization.

    chat.py: Handles Groq chat interactions and tool calling.

    data/data_processor.py: Manages data processing and formatting.

    data/fuzzy_engine.py: Contains the mathematical logic for the predictions.
