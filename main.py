import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup
import time





app =FastAPI()

def scrape_quotes_toscrape(soup):
    """Scrape quotes from http://quotes.toscrape.com."""
    quotes = []
    for quote in soup.find_all("div", class_="quote"):
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        quotes.append({"text": text, "author": author})
    return quotes

def scrape_quotes_goodreads(soup):
    """Scrape quotes from https://www.goodreads.com/quotes."""
    quotes = []
    for quote in soup.find_all("div", class_="quoteText"):
        text = quote.get_text(strip=True).split("―")[0].strip()
        author = quote.find("span", class_="authorOrTitle").text.strip()
        quotes.append({"text": text, "author": author})
    return quotes

@app.get("/", response_class=JSONResponse)
def getQuotes():
    headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    urls = [
        "http://quotes.toscrape.com",
        "https://www.goodreads.com/quotes"
    ]
    all_quotes = []

    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  
            soup = BeautifulSoup(response.text, "html.parser")
            time.sleep(1)
            
            if "toscrape" in url:
                quotes = scrape_quotes_toscrape(soup)
            elif "goodreads" in url:
                quotes = scrape_quotes_goodreads(soup)
            else:
                quotes = []

            all_quotes.extend(quotes)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

    return {"quotes": all_quotes}



if __name__ == "__main__":
    import uvicorn 
    uvicorn.run("main:app", host="127.0.0.1", port=8000,  reload=True)