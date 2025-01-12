from flask import Flask, render_template, request, jsonify
from scraper import WebScraper
import os

app = Flask(__name__)
scraper = WebScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    
    if not url:
        return render_template('index.html', error='URL is required')
    
    try:
        results = scraper.scrape(url)
        return render_template('index.html', results=results, url=url)
    except Exception as e:
        return render_template('index.html', error=str(e), url=url)

if __name__ == '__main__':
    app.run(debug=True)
