# README.md

```markdown
# Web Scraping Project

This project is a simple Flask app with a web scraper that performs data extraction from a web page and saves the results into a JSON file.

## Files
- `scraper.py`: Contains the `WebScraper` class used for scraping and data extraction.
- `main.py`: Application's main entry point. Contains request handlers for scraping data and retrieving results.

## Getting Started

To start the application, navigate to the project directory and run:

```
python main.py
```

This will start the Flask development server. You can access the application at `http://127.0.0.1:5000/`.

## How It Works

1. Send a POST request to `http://127.0.0.1:5000/scrape` with following JSON body:
```json
{
    "url": "<URL-of-the-Web-Page>",
    "selectors": {
    "<data-name>": "<css-selector>",
    ...
    }
}
```

This instructs the scraper to scrape the given URL and extract data according to the provided CSS selectors.

2. The extracted data is saved to a JSON file in the `data` directory.

3. GET request at `http://127.0.0.1:5000/results` will provide the JSON data that were parsed in last scrape.

## Error Handling

This app includes basic error handling. If a request to scrape a page fails due to a network error, the error will be logged and a corresponding HTTP status code 500 will be returned. 

If a required parameter (such as `url`) is missing from the request, a HTTP status code 400 will be returned.

## Coding Standards

Code in this project adheres to PEP 8 style guidelines.
```
```