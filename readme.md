# 📊 Instagram Influencer Analyzer

A web application that analyzes Instagram accounts and provides detailed metrics with an influencer score.

## Features

- 📈 Real-time Instagram data fetching
- 💯 Comprehensive scoring system (0-100)
- 📊 Detailed metrics breakdown
- 🎨 Beautiful, responsive UI
- ⚡ Fast and lightweight

## Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/instagram-influencer-analyzer.git
cd instagram-influencer-analyzer
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open http://localhost:5000 in your browser

## Deploy to Heroku

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Push to Heroku:
```bash
git push heroku main
```

4. Open your app:
```bash
heroku open
```

## Deploy to Render

1. Create account at [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Click "Create Web Service"

## Scoring Methodology

The score (0-100) is based on:
- **Engagement Quality (40%)**: Engagement rate + authenticity
- **Reach (25%)**: Follower count (logarithmic scale)
- **Content Quality (15%)**: Diversity + consistency
- **Credibility (10%)**: Verification + business account
- **Brand Collaboration (10%)**: Optimal collaboration balance

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Heroku / Render
- **API**: Instagram Web Profile API

## License

MIT License

## Contributing

Pull requests are welcome!
