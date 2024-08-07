import pprint
import re
from collections import Counter

from weasyprint import HTML
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns
import pandas as pd

from social_media.media_utils.pdf_utils import find_severity_score, analyse_severity

data = {
    'tweets': [
        {
            'original_tweet_text': 'Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M',
            'image_urls': ['https://pbs.twimg.com/media/GT_Ot1uXQAA_gW0?format=jpg&name=small',
                           'https://pbs.twimg.com/media/GUD1DkNWgAAFMfV?format=png&name=small',
                           'https://pbs.twimg.com/media/GT6DH3iWAAA6SFo?format=jpg&name=small'],
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
        },
        {
            'original_tweet_text': 'Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M',
            'image_urls': ['https://pbs.twimg.com/media/GT_Ot1uXQAA_gW0?format=jpg&name=small',
                           'https://pbs.twimg.com/media/GUD1DkNWgAAFMfV?format=png&name=small',
                           'https://pbs.twimg.com/media/GT6DH3iWAAA6SFo?format=jpg&name=small'],
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
        },
        {
            'original_tweet_text': 'Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M',
            'image_urls': ['https://pbs.twimg.com/media/GT_Ot1uXQAA_gW0?format=jpg&name=small',
                           'https://pbs.twimg.com/media/GUD1DkNWgAAFMfV?format=png&name=small',
                           'https://pbs.twimg.com/media/GT6DH3iWAAA6SFo?format=jpg&name=small'],
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
    ]
}

keywords = ['Israeli bombardment', 'bigotry', 'NourNaim88', 'gaza', 'jalalayn']

categories_keywords = {
    'religious': ['Allāh', 'Islam', 'pray', 'faith', 'spiritual', 'mosque', 'Quran'],
    'political': ['bombardment', 'Gaza', 'liberalism', 'racism', 'superiority', 'election', 'democracy'],
    'open_minded': ['tolerance', 'diversity', 'equality', 'freedom', 'inclusivity', 'acceptance'],
    'technology': ['AI', 'blockchain', 'cybersecurity', 'innovation', 'programming'],
    'health': ['wellness', 'nutrition', 'exercise', 'mental health', 'therapy']
}


def generate_chart(results):
    keywords = []
    scores = []
    for key, val in results.items():
        keywords.append(key + f" ({val['len']})")
        scores.append(val['matched'])

    # Create a DataFrame for the data
    data = pd.DataFrame({
        'Keywords': keywords,
        'Severity Score': scores
    })

    # Set a style
    sns.set(style="whitegrid")

    plt.figure(figsize=(6, 6))  # Size for better readability
    barplot = sns.barplot(data=data, y='Keywords', x='Severity Score', palette="viridis", hue='Keywords', dodge=False)

    plt.ylabel('', )
    plt.xlabel('')

    # Add value labels at the end of each bar and color them
    for index, (bar, value) in enumerate(zip(barplot.patches, scores)):
        bar_color = bar.get_facecolor()
        plt.text(value + 0.1, index, f'{value:.1f}', va='center', fontsize=10, weight='bold', color=bar_color)

    # Update y-axis label colors
    for label, bar in zip(barplot.get_yticklabels(), barplot.patches):
        label.set_color(bar.get_facecolor())

    # Remove legend
    plt.legend([], [], frameon=False)

    # Increase space on x-axis
    xlim = plt.xlim()
    plt.xlim(xlim[0], xlim[1] + 1)  # Extend the x-axis limit

    # Add grid lines
    barplot.xaxis.grid(True, color='gray', linestyle='dashed', linewidth=0.5)
    barplot.yaxis.grid(True, color='gray', linestyle='dashed', linewidth=0.5)

    # Adjust layout
    plt.tight_layout()

    # Save the plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


def generate_pdf(data, keywords, output_file='output.pdf'):
    results = analyse_severity(data, categories_keywords)
    chart_base64 = generate_chart(results)
    keyword_highlighter = "<span style='color:blue;'>"

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Social Media Analysis Report</title>
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
            .images-section {
                margin-top: 15px;
            }
            .images-section img {
                width: calc(33.33% - 10px);
                margin-right: 10px;
                margin-bottom: 10px;
                height: auto;
            }
            .links-section {
                margin-top: 15px;
            }
            .links-section a {
                color: #1a0dab;
                text-decoration: none;
            }
            .summary-table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
                text-align: center;
            }
            .summary-table th, .summary-table td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            .summary-table th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            .chart-container {
                text-align: center;
                margin: 20px 0;
            }
              td[colspan="2"] {
            background-color: #d9edf7;
        }
        </style>
    </head>
    <body>
        <header>
            Social Media Analysis Report
        </header>
        <div class="container">
            <h1>Graph Summary</h1>
            <div class="chart-container">
                <img src="data:image/png;base64, """ + chart_base64 + """" alt="Chart">
            </div>
            <h1>Summary Table</h1>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Severity Score</th>
                    </tr>
                </thead>
                <tbody>
    """

    for category, severity in results.items():
        html_content += f"""<tr>
            <td colspan="2">{category}</td>
        </tr>"""
        for keyword, severity_score in severity['counter'].items():
            html_content += f"""
                <tr>
                    <td>{keyword}</td>
                    <td>{severity_score}</td>
                </tr>
              
            """

    html_content += """
                </tbody>
            </table>
            <h1>Detailed Analysis</h1>
    """

    for tweet in data['tweets']:
        tweet_text = tweet['original_tweet_text']
        tweet_images = tweet.get('image_urls', [])
        tweet_links = tweet.get('links', [])
        # highlighted_tweet_text = tweet_text.replace(keyword, f"<span style='color:blue;'>{keyword}</span>")

        html_content += f"""
                <div class='tweet{' highlight' if keyword_highlighter in tweet_text else ''}'>
                    <div class='tweet-content'>{tweet_text}</div>
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
        <footer>
            Generated on: 2024-08-06
        </footer>
    </body>
    </html>
    """

    HTML(string=html_content).write_pdf(output_file)


# Example usage
generate_pdf(data, keywords)
