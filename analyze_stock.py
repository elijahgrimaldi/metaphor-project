from metaphor_python import Metaphor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bs4 import BeautifulSoup
from datetime import datetime

metaphor = Metaphor("a22ef647-a2dd-42ec-85ca-1e3f0b2d91d8")

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()



def clean_html(html_content):
    """Extract textual content from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


def get_articles_about_stock(stock_symbol, limit=50):
    # For the Metaphor search function, you might want to use the stock_symbol in the query.
    # The example given doesn't use the stock_symbol, so adjust accordingly.

    today = datetime.today().strftime('%Y-%m-%d')
    results = metaphor.search(f'Hottest 5 recent articles about {stock_symbol}',
                              num_results=5,
                              use_autoprompt=True,
                              start_published_date=today)
    content = []
    for result in results.results:
        response = metaphor.get_contents(result.id)
        for entry in response.contents:
            content.append(entry.extract)

    return content



def analyze_article_sentiment(article_html):
    # Clean the HTML content
    article_text = clean_html(article_html)
    
    # Splitting the article into paragraphs or segments
    segments = article_text.split('\n')
    segment_sentiments = []
    
    # Analyzing sentiment of each segment
    for segment in segments:
        if segment:  # Exclude empty segments
            sentiment = analyzer.polarity_scores(segment)
            segment_sentiments.append(sentiment['compound'])

    # Averaging the segment sentiments to determine overall article sentiment
    avg_sentiment = sum(segment_sentiments) / len(segment_sentiments)
    
    print(f"Average Sentiment for Article: {avg_sentiment:.2f}")
    
    # Sentiment determination based on averaged sentiment
    sentiment_difference = abs(sentiment['pos'] - sentiment['neg'])
    if sentiment_difference < 0.10:
        return "NEUTRAL"
    elif avg_sentiment >= 0.5:
        return "POSITIVE"
    elif avg_sentiment < 0.5:
        return "NEGATIVE"
    else:
        return "NEUTRAL"



def analyze_stock(stock_symbol):
    articles = get_articles_about_stock(stock_symbol)

    sentiment_counts = {
        "POSITIVE": 0,
        "NEGATIVE": 0,
        "NEUTRAL": 0
    }

    # Process the results
    for article in articles:
        sentiment = analyze_article_sentiment(article)
        sentiment_counts[sentiment] += 1

    # Enhanced Final Analysis Logic using ratios
    bullish_weight = sentiment_counts["POSITIVE"]
    bearish_weight = sentiment_counts["NEGATIVE"]
    neutral_weight = sentiment_counts["NEUTRAL"]

    overall_sentiment = ""
    if bullish_weight > 0 and bearish_weight > 0:
        sentiment_ratio = bullish_weight / bearish_weight
        if 0.8 < sentiment_ratio < 1.2:  # Example thresholds indicating a close race between bullish and bearish sentiments
            overall_sentiment = "NEUTRAL"
        elif sentiment_ratio > 1.2:
            overall_sentiment = "BULLISH"
        else:
            overall_sentiment = "BEARISH"
    elif bullish_weight > 0:
        overall_sentiment = "BULLISH"
    elif bearish_weight > 0:
        overall_sentiment = "BEARISH"
    else:
        overall_sentiment = "NEUTRAL"

    # Return both the overall sentiment and the sentiment counts
    return {
        "overall_sentiment": overall_sentiment,
        "sentiment_counts": sentiment_counts
    }
