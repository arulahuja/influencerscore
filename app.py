from flask import Flask, render_template, request, jsonify
from influencer_tracker import InfluencerTracker
from scorer import calculate_single_influencer_score
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Fetch Instagram data
        tracker = InfluencerTracker(username)
        
        if not tracker.fetch_data():
            return jsonify({'error': 'Failed to fetch data. Username may not exist or Instagram API is rate limiting.'}), 404
        
        # Get metrics
        profile = tracker.get_profile_metrics()
        engagement = tracker.get_engagement_metrics()
        content = tracker.get_content_analysis()
        
        if not profile or not engagement or not content:
            return jsonify({'error': 'Failed to process Instagram data'}), 500
        
        # Combine all data
        influencer_data = {
            **profile,
            **engagement,
            **content
        }
        
        # Calculate score
        score_data = calculate_single_influencer_score(influencer_data)
        
        # Combine everything
        result = {
            'username': username,
            'profile': profile,
            'engagement': engagement,
            'content': content,
            'score': score_data
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
