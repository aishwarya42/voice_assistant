import requests
import pyttsx3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak_route():
    data = request.form['text']
    speak(data)
    return jsonify({"message": "Text spoken successfully"})

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    api_key = "f0f5573f8380f273984957f642c87c60"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        temperature_celsius = temperature - 273.15
        return jsonify({"message": f"The weather in {city} is {weather_description} with a temperature of {temperature_celsius:.2f} degrees Celsius."})
    else:
        return jsonify({"error": "Sorry, I couldn't fetch the weather information for that city."})

@app.route('/get_news', methods=['GET'])
def get_news():
    api_key = "bae5f2726aee4d53b8708d2ffd943040"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "ok":
        articles = data["articles"]
        news = "Here are the top headlines for today:\n"
        for article in articles:
            news += article["title"] + "\n"
        return jsonify({"message": news})
    else:
        return jsonify({"error": "Sorry, I couldn't fetch the news for today."})

if __name__ == "__main__":
    app.run(debug=True)
