from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
from textblob import TextBlob
import random

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('moods.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS moods
                 (date TEXT, mood TEXT, notes TEXT, sentiment REAL, 
                  energy_level REAL, recommendation TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_mood_recommendations(mood, sentiment_score):
    prompts = {
        'happy': "To maintain your positive mood, you could try: ",
        'sad': "To help lift your spirits, consider: ",
        'anxious': "To help manage anxiety, try: ",
        'tired': "To boost your energy, you might want to: ",
        'stressed': "To reduce stress, consider: ",
        'neutral': "To enhance your day, you could: "
    }
    
    base_recommendations = {
        'happy': [
            "Share your joy with friends or family 🤗",
            "Start a creative project you've been thinking about ✨",
            "Practice gratitude journaling 📝",
        ],
        'sad': [
            "Take a gentle walk in nature 🌳",
            "Listen to uplifting music 🎵",
            "Reach out to a supportive friend 💝",
        ],
        'anxious': [
            "Try deep breathing exercises 🫁",
            "Practice mindfulness meditation 🧘‍♀️",
            "Write down your worries and possible solutions 📝",
        ],
        'tired': [
            "Take a power nap 😴",
            "Have a healthy energizing snack 🍎",
            "Do some light stretching 🧘‍♂️",
        ],
        'stressed': [
            "Take a relaxing bath 🛁",
            "Try progressive muscle relaxation 💆‍♀️",
            "Take short breaks between tasks ⏰",
        ],
        'neutral': [
            "Try something new today 🎯",
            "Connect with an old friend 👋",
            "Set a small goal for yourself ✅",
        ]
    }
    
    # Determine mood category
    mood_lower = mood.lower()
    mood_category = 'neutral'
    for key in base_recommendations:
        if key in mood_lower:
            mood_category = key
            break
    
    recommendations = base_recommendations[mood_category]
    return random.choice(recommendations)

@app.route('/log_mood', methods=['POST'])
def log_mood():
    data = request.json
    mood = data['mood']
    notes = data['notes']
    
    # Perform sentiment analysis using TextBlob
    text_to_analyze = notes if notes else mood
    analysis = TextBlob(text_to_analyze)
    sentiment_score = analysis.sentiment.polarity
    
    # Get AI recommendation
    recommendation = get_mood_recommendations(mood, sentiment_score)
    
    # Calculate energy level based on subjectivity
    energy_level = analysis.sentiment.subjectivity
    
    # Store in database
    conn = sqlite3.connect('moods.db')
    c = conn.cursor()
    c.execute('''INSERT INTO moods (date, mood, notes, sentiment, energy_level, recommendation)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
               mood, notes, sentiment_score, energy_level, recommendation))
    conn.commit()
    conn.close()
    
    return jsonify({
        'message': 'Mood logged successfully!',
        'sentiment': sentiment_score,
        'recommendation': recommendation
    })

@app.route('/mood_summary', methods=['GET'])
def get_mood_summary():
    conn = sqlite3.connect('moods.db')
    c = conn.cursor()
    c.execute('''SELECT date, mood, notes, sentiment, energy_level, recommendation 
                 FROM moods ORDER BY date DESC''')
    data = c.fetchall()
    conn.close()
    
    # Calculate mood trends and patterns
    if data:
        avg_sentiment = sum(row[3] for row in data) / len(data)
        avg_energy = sum(row[4] for row in data) / len(data)
    else:
        avg_sentiment = 0
        avg_energy = 0
    
    return jsonify({
        'data': data,
        'analytics': {
            'average_sentiment': avg_sentiment,
            'average_energy': avg_energy
        }
    })

if __name__ == '__main__':
    app.run(debug=True) 