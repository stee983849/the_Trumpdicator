# The Trumpdicator

A tool that scrapes Donald Trump's posts from Twitter and other sources to provide immediate advice on affected industries and stocks with bullish/bearish signals.

## Features

- Real-time scraping of Trump's posts from Twitter and other sources
- Analysis of posts to identify affected industries and stocks
- Generation of bullish/bearish signals based on post content
- User-friendly dashboard to view latest posts, signals, and historical performance

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file:
   ```
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_SECRET=your_access_secret
   NEWS_API_KEY=your_news_api_key
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```
2. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `/scrapers`: Contains modules for scraping Trump's posts from various sources
- `/analysis`: Contains modules for analyzing posts and generating signals
- `/data`: Stores scraped posts, generated signals, and historical data
- `/templates`: HTML templates for the web interface
- `/static`: CSS and JavaScript files for the web interface

## Disclaimer

This tool is for informational purposes only and should not be considered financial advice. Always do your own research before making investment decisions.