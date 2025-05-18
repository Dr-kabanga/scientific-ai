import requests

def get_random_joke():
    """Fetches a random joke from the Official Joke API and returns it as a string."""
    url = "https://official-joke-api.appspot.com/jokes/random"
    try:
        response = requests.get(url)
        response.raise_for_status()
        joke_data = response.json()
        setup = joke_data.get("setup", "No joke found.")
        punchline = joke_data.get("punchline", "")
        return f"{setup}\n{punchline}"
    except requests.RequestException as e:
        return f"Error fetching joke: {e}"

if __name__ == "__main__":
    print("Here's a random joke for you:\n")
    print(get_random_joke())