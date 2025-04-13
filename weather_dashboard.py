# Import necessary libraries
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Replace with a free weather API key from OpenWeatherMap or similar service
API_KEY = "your_api_key_here"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            params = {"q": city, "appid": API_KEY, "units": "metric"}
            try:
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()
                weather_data = response.json()
            except requests.exceptions.RequestException as e:
                error = f"Error fetching weather data: {e}"
        else:
            error = "Please enter a city name."

    return render_template("index.html", weather_data=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)