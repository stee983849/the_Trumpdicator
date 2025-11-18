import os
import json
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Import real components with graceful fallbacks
try:
    from scrapers.twitter_scraper import TwitterScraper
except Exception:
    TwitterScraper = None

try:
    from scrapers.news_scraper import NewsScraper
except Exception:
    NewsScraper = None

try:
    from analysis.impact_analyzer import ImpactAnalyzer
except Exception:
    ImpactAnalyzer = None

# Minimal SignalGenerator placeholder (can be replaced with a real one later)
class SimpleSignalGenerator:
    def generate_signals(self, industry_impacts):
        industry_signals = []
        stock_signals = []

        for industry, data in industry_impacts.items():
            sentiment = data.get("sentiment", "neutral")
            strength = min(1.0, max(0.0, data.get("impact_score", 0) / 10))
            signal_type = "neutral"
            if sentiment == "positive":
                signal_type = "bullish"
            elif sentiment == "negative":
                signal_type = "bearish"

            industry_signals.append({
                "industry": industry.title(),
                "signal_type": signal_type,
                "strength": strength,
                "description": f"Detected {sentiment} sentiment with impact score {data.get('impact_score', 0)}",
                "related_stocks": data.get("affected_stocks", [])
            })

            for s in data.get("affected_stocks", []):
                stock_signals.append({
                    "symbol": s,
                    "company": s,
                    "signal_type": signal_type,
                    "strength": strength,
                    "industry": industry.title()
                })

        return {"industry_signals": industry_signals, "stock_signals": stock_signals}

# Initialize components
twitter_scraper = TwitterScraper() if TwitterScraper else None
news_scraper = NewsScraper() if NewsScraper else None
impact_analyzer = ImpactAnalyzer() if ImpactAnalyzer else None
signal_generator = SimpleSignalGenerator()
# Data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
POSTS_FILE = os.path.join(DATA_DIR, 'posts.csv')
SIGNALS_FILE = os.path.join(DATA_DIR, 'signals.json')
HISTORICAL_FILE = os.path.join(DATA_DIR, 'historical.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        # Check if we need to refresh data
        refresh = request.args.get('refresh', 'false').lower() == 'true'
        
        if refresh:
            # Scrape new data
            twitter_posts = []
            news_posts = []
            try:
                if twitter_scraper:
                    twitter_posts = twitter_scraper.get_trump_posts()
            except Exception:
                twitter_posts = []
            try:
                if news_scraper:
                    news_posts = news_scraper.get_trump_mentions()
            except Exception:
                news_posts = []
            
            # Combine posts
            all_posts = twitter_posts + news_posts
            
            # Sort by timestamp (newest first)
            all_posts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Save to CSV
            if all_posts:
                df = pd.DataFrame(all_posts)
                df.to_csv(POSTS_FILE, index=False)
        else:
            # Load from CSV if it exists
            if os.path.exists(POSTS_FILE):
                df = pd.read_csv(POSTS_FILE)
                all_posts = df.to_dict('records')
            else:
                # Generate sample data if no file exists
                all_posts = generate_sample_posts()
                
                # Save sample data
                df = pd.DataFrame(all_posts)
                df.to_csv(POSTS_FILE, index=False)
        
        # Return only the latest 10 posts
        latest_posts = all_posts[:10] if all_posts else []
        
        return jsonify({
            'success': True,
            'posts': latest_posts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/signals', methods=['GET'])
def get_signals():
    try:
        # Check if we need to refresh data
        refresh = request.args.get('refresh', 'false').lower() == 'true'
        
        if refresh:
            # Load the latest posts
            if os.path.exists(POSTS_FILE):
                posts_df = pd.read_csv(POSTS_FILE)
                posts = posts_df.to_dict('records')
            else:
                posts = generate_sample_posts()
            
            # Analyze posts for industry impacts
            if impact_analyzer:
                industry_impacts = impact_analyzer.analyze_posts(posts)
            else:
                industry_impacts = {}
            
            # Generate signals based on impacts
            signals = signal_generator.generate_signals(industry_impacts)
            
            # Save signals to JSON
            with open(SIGNALS_FILE, 'w') as f:
                json.dump(signals, f)
        else:
            # Load from JSON if it exists
            if os.path.exists(SIGNALS_FILE):
                with open(SIGNALS_FILE, 'r') as f:
                    signals = json.load(f)
            else:
                # Generate sample signals if no file exists
                signals = generate_sample_signals()
                
                # Save sample signals
                with open(SIGNALS_FILE, 'w') as f:
                    json.dump(signals, f)
        
        # Extract industry and stock signals
        industry_signals = signals.get('industry_signals', [])
        stock_signals = signals.get('stock_signals', [])
        
        return jsonify({
            'success': True,
            'industry_signals': industry_signals,
            'stock_signals': stock_signals
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/historical', methods=['GET'])
def get_historical():
    try:
        # Load from JSON if it exists
        if os.path.exists(HISTORICAL_FILE):
            with open(HISTORICAL_FILE, 'r') as f:
                historical_data = json.load(f)
        else:
            # Generate sample historical data if no file exists
            historical_data = generate_sample_historical()
            
            # Save sample data
            with open(HISTORICAL_FILE, 'w') as f:
                json.dump(historical_data, f)
        
        return jsonify({
            'success': True,
            'historical_data': historical_data.get('data', []),
            'accuracy_stats': historical_data.get('accuracy_stats', {})
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Sample data generators for demonstration
def generate_sample_posts():
    now = datetime.now()
    
    sample_posts = [
        {
            'id': '1',
            'author': 'Donald J. Trump',
            'content': 'Just got off the phone with Elon Musk. We discussed the future of electric vehicles and space exploration. American innovation is the best in the world! Tesla and SpaceX are doing incredible things.',
            'timestamp': (now - timedelta(hours=2)).isoformat(),
            'source': 'Twitter',
            'profile_image': 'https://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_400x400.jpg',
            'url': 'https://twitter.com/user/status/1'
        },
        {
            'id': '2',
            'author': 'Donald J. Trump',
            'content': 'The pharmaceutical industry needs to lower drug prices NOW! Americans are paying too much for prescription drugs. Time for Big Pharma to step up and do what\'s right for our great citizens!',
            'timestamp': (now - timedelta(hours=5)).isoformat(),
            'source': 'Twitter',
            'profile_image': 'https://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_400x400.jpg',
            'url': 'https://twitter.com/user/status/2'
        },
        {
            'id': '3',
            'author': 'Donald J. Trump',
            'content': 'Just signed a major Executive Order on defense spending. We\'re going to rebuild our military like never before. Lockheed Martin, Boeing, and Raytheon will be very busy. AMERICA FIRST!',
            'timestamp': (now - timedelta(hours=8)).isoformat(),
            'source': 'Twitter',
            'profile_image': 'https://pbs.twimg.com/profile_images/874276197357596672/kUuht00m_400x400.jpg',
            'url': 'https://twitter.com/user/status/3'
        }
    ]
    
    return sample_posts

def generate_sample_signals():
    sample_signals = {
        'industry_signals': [
            {
                'industry': 'Automotive & Electric Vehicles',
                'signal_type': 'bullish',
                'strength': 0.85,
                'description': 'Positive sentiment toward Tesla and electric vehicle innovation',
                'related_stocks': ['TSLA', 'GM', 'F']
            },
            {
                'industry': 'Aerospace & Defense',
                'signal_type': 'bullish',
                'strength': 0.92,
                'description': 'Increased defense spending and support for major contractors',
                'related_stocks': ['LMT', 'BA', 'RTX']
            },
            {
                'industry': 'Pharmaceuticals',
                'signal_type': 'bearish',
                'strength': 0.78,
                'description': 'Pressure to lower drug prices could impact profit margins',
                'related_stocks': ['PFE', 'JNJ', 'MRK']
            }
        ],
        'stock_signals': [
            {
                'symbol': 'TSLA',
                'company': 'Tesla Inc.',
                'signal_type': 'bullish',
                'strength': 0.88,
                'industry': 'Automotive & Electric Vehicles'
            },
            {
                'symbol': 'LMT',
                'company': 'Lockheed Martin Corp.',
                'signal_type': 'bullish',
                'strength': 0.94,
                'industry': 'Aerospace & Defense'
            },
            {
                'symbol': 'PFE',
                'company': 'Pfizer Inc.',
                'signal_type': 'bearish',
                'strength': 0.79,
                'industry': 'Pharmaceuticals'
            }
        ]
    }
    
    return sample_signals

def generate_sample_historical():
    now = datetime.now()
    
    # Generate dates for the past 30 days
    dates = [(now - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
    
    # Generate sample historical data
    data = []
    
    import random
    random.seed(42)  # For reproducibility
    
    for date in dates:
        bullish_accuracy = 0.5 + random.uniform(-0.2, 0.4)  # Between 0.3 and 0.9
        bearish_accuracy = 0.5 + random.uniform(-0.2, 0.4)  # Between 0.3 and 0.9
        
        data.append({
            'date': date,
            'bullish_accuracy': bullish_accuracy,
            'bearish_accuracy': bearish_accuracy,
            'total_signals': random.randint(5, 20)
        })
    
    # Calculate overall accuracy stats
    total_bullish = sum(item['bullish_accuracy'] * item['total_signals'] for item in data)
    total_bearish = sum(item['bearish_accuracy'] * item['total_signals'] for item in data)
    total_signals = sum(item['total_signals'] for item in data)
    
    accuracy_stats = {
        'overall_accuracy': (total_bullish + total_bearish) / (2 * total_signals) if total_signals > 0 else 0,
        'bullish_accuracy': total_bullish / total_signals if total_signals > 0 else 0,
        'bearish_accuracy': total_bearish / total_signals if total_signals > 0 else 0,
        'total_signals': total_signals
    }
    
    return {
        'data': data,
        'accuracy_stats': accuracy_stats
    }

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Run the app - host='0.0.0.0' makes it accessible from any IP
    # Using port 5001 to avoid conflicts with AirPlay on macOS
    # Using port 5001 to avoid conflicts with AirPlay on macOS
    app.run(debug=True, host='0.0.0.0', port=5001)