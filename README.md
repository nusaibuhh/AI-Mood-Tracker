# AI Mood Journal

An intelligent mood tracking application that uses AI to analyze your emotions and provide personalized recommendations.

## Features

- 📝 Daily mood tracking with notes
- 🤖 AI-powered sentiment analysis
- 📊 Visual mood trends and analytics
- 💡 Personalized recommendations based on your mood
- 📈 Energy level tracking
- ✨ Beautiful, responsive UI with animations

## Technologies Used

- Frontend: HTML, CSS, JavaScript with Chart.js
- Backend: Python Flask
- AI: TextBlob for sentiment analysis
- Database: SQLite

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-mood-journal
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Download required NLTK data:
```bash
python download_nltk_data.py
```

4. Start the Flask backend:
```bash
python app.py
```

5. Open `index.html` in your web browser

## Usage

1. Enter your current mood and optional notes
2. The AI will analyze your mood and provide personalized recommendations
3. View your mood trends and analytics in the charts
4. Track your progress over time in the mood history table

## Project Structure

- `app.py` - Flask backend with AI functionality
- `index.html` - Frontend user interface
- `styles.css` - CSS styles and animations
- `requirements.txt` - Python dependencies
- `download_nltk_data.py` - Script to download required NLTK data

## Contributing

Feel free to submit issues and enhancement requests! 