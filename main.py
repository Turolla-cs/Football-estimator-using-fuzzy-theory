from chatbot.chat import activate


if __name__ == "__main__":
    print("--- Soccer Match Prediction System Initialized ---")
    print("\nSystem is ready to analyze games based on Fuzzy Logic.")
    try:
        activate()
    except KeyboardInterrupt:
        print("\nSystem shutting down. Goodbye!")