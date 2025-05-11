
from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import random
import csv

app = Flask(__name__)

coping_strategies = []
wellness_routines = []
therapist_contacts = {}

def load_data_from_csv(filename="mental_health_data.csv"):
    global coping_strategies, wellness_routines, therapist_contacts
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = row.get('Category')
                text = row.get('Text')
                country = row.get('Country')
                name = row.get('Name')
                contact = row.get('Contact')
                website = row.get('Website')
                description = row.get('Description')

                if category == 'coping_strategy' and text:
                    coping_strategies.append(text)
                elif category == 'wellness_routine' and text:
                    wellness_routines.append(text)
                elif category == 'therapist_contact' and country and name and contact:
                    if country not in therapist_contacts:
                        therapist_contacts[country] = []
                    therapist_contacts[country].append({
                        'name': name,
                        'contact': contact,
                        'website': website,
                        'description': description
                    })
    except FileNotFoundError:
        coping_strategies.extend([
            "Take deep breaths and count to ten.",
            "Engage in a hobby you love.",
            "Talk to a friend or family member.",
            "Practice mindfulness or meditation.",
            "Write down your thoughts in a journal."
        ])
        wellness_routines.extend([
            "Maintain a regular sleep schedule.",
            "Exercise for at least 30 minutes a day.",
            "Eat balanced and nutritious meals.",
            "Stay hydrated by drinking enough water.",
            "Set aside time for relaxation and self-care."
        ])
        therapist_contacts["India"] = [
            {"name": "iCall", "contact": "+91-9152987821", "website": "https://icallhelpline.org/", "description": "Phone and email-based counseling."},
            {"name": "Vandrevala Helpline", "contact": "1860 266 2345", "website": "http://www.vandrevalafoundation.com/", "description": "24x7 crisis support."},
            {"name": "AASRA", "contact": "+91-9820466726", "website": "http://www.aasra.info/", "description": "Suicide prevention support."}
        ]

load_data_from_csv()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.5:
        mood = "positive"
        suggestion = random.choice([
            "Engage in a creative project.",
            "Spend time with loved ones.",
            "Help someone else.",
            "Set a new goal and work towards it.",
            "Enjoy your favorite music or movie."
        ])
        response = f"You're feeling good! Try this: {suggestion}"
    elif polarity < -0.5:
        mood = "negative"
        coping = random.choice(coping_strategies)
        routine = random.choice(wellness_routines)
        response = f"It seems you're feeling down. Try this coping strategy: {coping} and wellness tip: {routine}."
    else:
        mood = "neutral"
        suggestion = random.choice(wellness_routines)
        response = f"Thanks for sharing. Here's a wellness tip: {suggestion}"
    return jsonify({"mood": mood, "response": response})

@app.route("/therapist", methods=["POST"])
def therapist_info():
    data = request.json
    country = data.get("country", "India").capitalize()
    contacts = therapist_contacts.get(country, [])
    if not contacts:
        return jsonify({"info": f"No therapist data for {country}."})
    info = f"Therapists in {country}:
"
    for t in contacts:
        info += f"- {t['name']} ({t['contact']}) - {t['description']} - {t['website']}
"
    return jsonify({"info": info})

if __name__ == "__main__":
    app.run(debug=True)
