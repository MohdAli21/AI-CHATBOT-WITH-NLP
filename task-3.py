import requests
import sympy as sp
import random
from nltk.chat.util import Chat, reflections

# Your API keys (Replace with your own keys)
WEATHER_API_KEY = "ff5395904ab7f5c7352c6271cf9e5836"
NEWS_API_KEY = "0031041e1a2443d799308fddf31b9210"

# Function to get weather updates
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url).json()
        if response["cod"] == 200:
            temp = response["main"]["temp"]
            weather_desc = response["weather"][0]["description"]
            return f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."
        else:
            return "Sorry, I couldn't fetch the weather. Please check the city name."
    except:
        return "Error retrieving weather data."

# Function to fetch general worldwide news with randomization
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?category=general&pageSize=10&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])  # Fetch all articles
        if not articles:
            return "No worldwide news found."

        random_articles = random.sample(articles, min(3, len(articles)))  # Pick 3 unique random articles
        news_list = [f"{i+1}. {article['title']}" for i, article in enumerate(random_articles)]
        return "\n".join(news_list)
    except:
        return "Error fetching news."

# Function to solve math expressions
def solve_math(expression):
    try:
        return str(sp.sympify(expression))
    except:
        return "Invalid math expression!"

# Function to tell programming-related jokes
def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the Python programmer break up with Java? Because it had too many exceptions!",
        "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
        "Why do Java developers wear glasses? Because they don’t C#!",
        "Debugging: Being the detective in a crime movie where YOU are also the murderer.",
        "Why don’t programmers like nature? It has too many bugs.",
        "How many programmers does it take to change a light bulb? None, that’s a hardware issue!"
    ]
    return random.choice(jokes)

# Define chatbot responses
pairs = [
    (r'hi|hello|hey', ['Hello!', 'Hey there!', 'Hi! How can I help you?']),
    (r'how are you?', ['I am good, thank you!', 'I am just a bot, but I am functioning properly!']),
    (r'what is your name?', ['I am a chatbot created to assist you.', 'You can call me ChatBot!']),
    (r'what can you do?', ['I can provide weather updates, tell jokes, fetch news, and solve math problems!']),
    (r'weather', ['Enter the city name']),  # Asks for city name
    (r'news|what\'s today\'s news', ['Fetching the latest news...']),
    (r'tell me a joke', ['Here’s a joke for you:']),
    (r'solve (.*)', ['Let me solve that for you!']),
    (r'bye|goodbye', ['Goodbye! Have a great day!', 'Bye! Take care!']),
    (r'(.*)', ['I am not sure how to respond to that.', 'Can you rephrase your question?'])
]

# Create chatbot instance
chatbot = Chat(pairs, reflections)

print("Hello! I am your chatbot. Type 'bye' to exit.")
while True:
    user_input = input('You: ').lower()
    
    if user_input in ['bye', 'goodbye']:
        print("Chatbot: Goodbye! Have a great day!")
        break

    response = chatbot.respond(user_input)
    
    # Weather handling
    if response == "Enter the city name":
        city = input("Chatbot: Enter the city name: ")
        response = get_weather(city)
    
    # News handling
    elif "Fetching the latest news..." in response:
        response = get_news()
    
    # Jokes handling
    elif "Here’s a joke for you:" in response:
        response = tell_joke()
    
    # Math solving
    elif "Let me solve that for you!" in response:
        expression = user_input.split("solve ")[1]
        response = solve_math(expression)

    print(f"Chatbot: {response}")
