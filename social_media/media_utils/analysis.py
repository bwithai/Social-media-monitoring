import os

from weasyprint import HTML

from social_media.media_utils.pdf_utils import find_severity_score_based_on_post_data
from utils import get_current_pakistan_time
import database

# Get the path to the 'database' module directory
module_path = os.path.dirname(database.__file__)

# Construct the path to 'pdf_db' directory
pdf_db_path = os.path.join(module_path, 'pdf_db')


def generate_pdf(data, keyword, output_file='Analysis.pdf'):
    output_file = f"{pdf_db_path}/{output_file}"
    severity_score, filtered_tweets, percentage = find_severity_score_based_on_post_data(data, keyword)
    keyword_highlighter = '<span style=\'color:blue;\'>'

    # Generate HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Social Media Analysis Report</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');
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
                padding: 8px;
            }
            .container {
                max-width: 800px;
                margin: auto;
                background: #fff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }
            .section {
                margin: 20px 0;
                padding: 10px 0;
                border-bottom: 1px solid #eee;
            }
            .tweet, .post {
                border: 1px solid #ddd;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                background-color: #fefefe;
            }
            .tweet.highlight, .post.highlight {
                background-color: #fff8c6;
            }
            .tweet-header, .post-header {
                font-weight: 700;
                margin-bottom: 10px;
            }
            .tweet-content, .post-content {
                line-height: 1.6;
            }
            .highlight {
                background-color: yellow;
                color: red;
            }
            .image {
                display: inline-block;
                padding-left: 10px;
                margin: 10px auto; /* Centers the image horizontally and adds top margin */
                max-width: 150px; /* Set the maximum width you desire */
                max-height: 180px; /* Set the maximum height you desire */
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .images-section, .links-section {
                margin-top: 15px;
                padding: 10px;
                background-color: #f7f7f7;
                border-radius: 8px;
            }
            .images-section h4, .links-section h4 {
                margin: 0 0 10px;
                font-size: 1.1em;
                color: #4CAF50;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }
            header {
                text-align: center;
                padding: 10px 0;
                margin-top: -60px;
                margin-left: -8px;
                width: 640px;
                background-color: #336600;
                color: #fff;
                font-size: 1.5em;
                border-top-left-radius: 50%; /* Upper left corner */
                border-top-right-radius: 50%; /* Upper right corner */
            }
            footer {
                text-align: center;
                padding: 10px 0;
                width: 640px;
                margin-left: -8px;
                background-color: #336600;
                color: #fff;
                font-size: 1.5em;
                border-bottom-left-radius: 50%; /* Upper left corner */
                border-bottom-right-radius: 50%; /* Upper right corner */
            }
            .header, .footer {
                max-width: 800px;
                margin: 0 auto;
                padding: 0 20px;
                box-sizing: border-box;
            }
            h1 {
                font-size: 2em;
                color: #333;
                text-align: center;
                margin: 20px 0;
            }
            h2 {
                font-size: 1.5em;
                color: #4CAF50;
                margin: 20px 0 10px;
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 5px;
            }
            h3 {
                font-size: 1.2em;
                color: #777;
                margin: 10px 0;
                padding-bottom: 5px;
            }
        </style>
    </head>
    <body>
        <header>
            <div class="header" style='font-family: Lobster, cursive;'>
                101 Analysis Report
            </div>
        </header>
        <div class="container">
            <h1>Analysis Report</h1>
            <div class="section">
                <h2>Section 1: Tweets</h2>
                <h3>Subsection 1.1: Keyword Analysis</h3>
    """

    for tweet in data['tweets']:
        tweet_text = tweet['original_description']
        tweet_images = tweet.get('images', [])
        tweet_links = tweet.get('links', [])
        highlighted_tweet_text = tweet_text.replace(keyword, f"<span style='color:blue;'>{keyword}</span>")

        html_content += f"""
        <div class='tweet{' highlight' if keyword_highlighter in tweet_text else ''}'>
            <div class='tweet-content'>{highlighted_tweet_text}</div>
        """

        if tweet_images:
            html_content += "<div class='images-section'><h4>Images</h4>"
            for image_url in tweet_images:
                html_content += f"<img src='{image_url}' class='image'/>"
            html_content += "</div>"

        if tweet_links:
            html_content += "<div class='links-section'><h4>Links</h4><ul>"
            for link in tweet_links:
                html_content += f"<li><a href='{link}'>{link}</a></li>"
            html_content += "</ul></div>"

        html_content += "</div>"

    html_content += """
            </div>
            <div class="section">
                <h2>Section 2: Facebook Posts</h2>
                <h3>Subsection 2.1: Post Analysis</h3>
    """

    for post in data['fb_posts']:
        post_text = post['original_description']
        post_images = post.get('images', [])
        post_links = post.get('links', [])
        highlighted_post_text = post_text.replace(keyword, f"<span style='color:blue;'>{keyword}</span>")

        html_content += f"""
        <div class='post{' highlight' if keyword_highlighter in post_text else ''}'>
            <div class='post-content'>{highlighted_post_text}</div>
        """

        if post_images:
            html_content += "<div class='images-section'><h4>Images</h4>"
            for image_url in post_images:
                html_content += f"<img src='{image_url}' class='image'/>"
            html_content += "</div>"

        if post_links:
            html_content += "<div class='links-section'><h4>Links</h4><ul>"
            for link in post_links:
                html_content += f"<li><a href='{link}'>{link}</a></li>"
            html_content += "</ul></div>"

        html_content += "</div>"

    html_content += f"""
            </div>
        </div>
        <footer>
            <div class="footer">
                Generated on: {get_current_pakistan_time()}
            </div>
        </footer>
    </body>
    </html>
    """

    # Convert HTML to PDF
    HTML(string=html_content).write_pdf(output_file)
