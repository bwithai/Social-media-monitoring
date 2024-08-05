from weasyprint import HTML
import unidecode

data = {
    'tweets': [
        {
            'original_tweet_text': 'Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M',
            'image_urls': ['https://pbs.twimg.com/media/GT_Ot1uXQAA_gW0?format=jpg&name=small', 'https://pbs.twimg.com/media/GUD1DkNWgAAFMfV?format=png&name=small', 'https://pbs.twimg.com/media/GT6DH3iWAAA6SFo?format=jpg&name=small'],
            'links': ['https://example.com', 'https://anotherexample.com']
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K',
            'image_urls': ['https://pbs.twimg.com/media/GT6DH3iWAAA6SFo?format=jpg&name=small'],
            'links': []
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K',
            'image_urls': [],
            'links': ['https://example.com']
        }
    ],
    'facebook_posts': [
        {
            'original_post_text': 'John Doe\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244 likes\n3.2K comments',
            'image_urls': ['https://via.placeholder.com/150'],
            'links': ['https://example.com']
        },
        {
            'original_post_text': 'Jane Smith\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436 likes\n11K comments',
            'image_urls': ['https://via.placeholder.com/150', 'https://via.placeholder.com/200'],
            'links': ['https://anotherexample.com']
        },
        {
            'original_post_text': 'John Doe\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\n5 likes\n80 comments',
            'image_urls': [],
            'links': []
        }
    ]
}

def find_severity_score(data, keyword):
    # Normalize the keyword for comparison
    normalized_keyword = unidecode.unidecode(keyword).lower()
    highlighted_keyword = f"<span style='color:blue;'>{keyword}</span>"

    # Flatten the list of tweet texts
    tweet_texts = [tweet['original_tweet_text'] for tweet in data['tweets']]

    # Filter tweet texts containing the keyword, with normalization and highlight
    filtered_tweets = [
        tweet.replace(keyword, highlighted_keyword)
        for tweet in tweet_texts
        if normalized_keyword in unidecode.unidecode(tweet).lower()
    ]

    # Severity score is the count of filtered tweet texts
    severity_score = len(filtered_tweets)

    # Calculate the percentage
    percentage = round((severity_score / len(tweet_texts)) * 100, 2)

    return severity_score, filtered_tweets, percentage

def generate_pdf(data, keyword, output_file='output.pdf'):
    severity_score, filtered_tweets, percentage = find_severity_score(data, keyword)

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
                padding: 0;
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
                max-height: 150px; /* Set the maximum height you desire */
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
                padding: 20px 0;
                background-color: #4CAF50;
                color: #fff;
                font-size: 1.5em;
                font-family: 'Lobster', cursive;
                position: running(header);
            }
            footer {
                text-align: center;
                padding: 10px 0;
                background-color: #4CAF50;
                color: #fff;
                font-size: 1em;
                position: running(footer);
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
            <div class="header">
                Social Media Analysis Report
            </div>
        </header>
        <div class="container">
            <h1>Analysis Report</h1>
            <div class="section">
                <h2>Section 1: Tweets</h2>
                <h3>Subsection 1.1: Keyword Analysis</h3>
    """

    for tweet in data['tweets']:
        tweet_text = tweet['original_tweet_text']
        tweet_images = tweet.get('image_urls', [])
        tweet_links = tweet.get('links', [])
        highlighted_tweet_text = tweet_text.replace(keyword, f"<span style='color:blue;'>{keyword}</span>")

        html_content += f"""
        <div class='tweet{' highlight' if unidecode.unidecode(keyword).lower() in unidecode.unidecode(tweet_text).lower() else ''}'>
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

    for post in data['facebook_posts']:
        post_text = post['original_post_text']
        post_images = post.get('image_urls', [])
        post_links = post.get('links', [])
        highlighted_post_text = post_text.replace(keyword, f"<span style='color:blue;'>{keyword}</span>")

        html_content += f"""
        <div class='post{' highlight' if unidecode.unidecode(keyword).lower() in unidecode.unidecode(post_text).lower() else ''}'>
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

    html_content += """
            </div>
        </div>
        <footer>
            <div class="footer">
                Generated on: 2024-08-02
            </div>
        </footer>
    </body>
    </html>
    """

    # Convert HTML to PDF
    HTML(string=html_content).write_pdf(output_file)

# Example usage
keyword = 'Israeli bombardment'
generate_pdf(data, keyword)
