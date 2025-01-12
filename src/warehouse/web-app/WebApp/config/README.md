# Web Scraper

A web scraping application built with Beautiful Soup and Flask.

## Features

- Web page scraping using Beautiful Soup
- Data extraction using CSS selectors
- JSON data storage
- Web interface for easy interaction

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Enter the URL you want to scrape
2. Specify CSS selectors in JSON format
3. Click "Start Scraping"
4. View the results in JSON format
