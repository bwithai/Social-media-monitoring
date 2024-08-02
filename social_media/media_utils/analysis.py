from weasyprint import HTML

from social_media.media_utils.pdf_utils import find_severity_score_based_on_post_data
from utils import get_current_pakistan_time


def generate_pdf(tweets_data, keyword, output_file='output.pdf'):
    severity_score, filtered_tweets, percentage = find_severity_score_based_on_post_data(tweets_data, keyword)

    # Generate HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Tweets PDF</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

            @page {
                size: A4;
                margin: 20mm;
                @top-center {
                    content: element(header);
                }
                @bottom-center {
                    content: element(footer);
                }
            }

            body {
                font-family: 'Roboto', sans-serif;
                background-color: #f9f9f9;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: #fff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .tweet {
                border: 1px solid #ddd;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .tweet.highlight {
                background-color: #fff8c6;
            }
            .tweet-header {
                font-weight: 700;
                margin-bottom: 10px;
            }
            .tweet-content {
                line-height: 1.6;
            }
            .tweet-footer {
                margin-top: 10px;
                font-size: 0.9em;
                color: #555;
            }
            .highlight {
                background-color: yellow;
                color: red;
            }
            header {
                text-align: center;
                padding: 10px 0;
                margin-top: -60px;
                margin-left: -19px;
                width: 640px;
                background-color: #333;
                color: #fff;
                font-size: 1.2em;
                border-top-left-radius: 50%; /* Upper left corner */
                border-top-right-radius: 50%; /* Upper right corner */
            }
            footer {
                text-align: center;
                padding: 10px 0;
                margin-left: -19px;
                width: 640px;
                background-color: #333;
                color: #fff;
                font-size: 1.2em;
                border-bottom-left-radius: 50%; /* Upper left corner */
                border-bottom-right-radius: 50%; /* Upper right corner */
            }
        </style>
    </head>
    <body>
        <header>
            Tweets Analysis Report
        </header>
        <div class="container">
    """

    for tweet in tweets_data[0]['tweets']:
        tweet_text = tweet['original_tweet_text']
        # highlighted_tweet_text = tweet_text.replace(keyword, f"<span style='color:blue;'>{keyword}</span>")

        if '<span style=\'color:blue;\'>' in tweet_text:
            html_content += f"<div class='tweet highlight'><div class='tweet-content'>{tweet_text}</div></div>"
        else:
            html_content += f"<div class='tweet'><div class='tweet-content'>{tweet_text}</div></div>"

    html_content += f"""
        </div>
        <footer>
            Generated on: {get_current_pakistan_time()}
        </footer>
    </body>
    </html>
    """

    # Convert HTML to PDF
    HTML(string=html_content).write_pdf(output_file)
