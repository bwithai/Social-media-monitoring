import pprint
import re

from weasyprint import HTML
import unidecode

from utils import get_current_pakistan_time

tweets_data = [
    {'tweets': [
        {
            'original_tweet_text': 'Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K'
        },
        {
            'original_tweet_text': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K'
        }
    ]}
]


def find_severity_score(tweets_data, keyword):
    # Normalize the keyword for comparison
    normalized_keyword = unidecode.unidecode(keyword).lower()
    highlighted_keyword = f"<span style='color:blue;'>{keyword}</span>"

    # Compile a regex pattern for case-insensitive matching
    keyword_pattern = re.compile(re.escape(normalized_keyword), re.IGNORECASE)

    severity_score = 0

    # Function to highlight the keyword while preserving original text
    def highlight_match(match):
        return f"<span style='color:blue;'>{match.group(0)}</span>"

    # Iterate over tweets and replace the keyword with highlighted_keyword
    for tweet in tweets_data[0]['tweets']:
        tweet_text = tweet['original_tweet_text']
        if keyword_pattern.search(unidecode.unidecode(tweet_text).lower()):
            tweet['original_tweet_text'] = keyword_pattern.sub(highlight_match, tweet_text)
            severity_score += 1

    # Calculate the percentage
    percentage = round((severity_score / len(tweets_data[0]['tweets'])) * 100, 2)

    # Collect filtered tweets for output
    filtered_tweets = [
        tweet['original_tweet_text'] for tweet in tweets_data[0]['tweets']
        if highlighted_keyword in tweet['original_tweet_text']
    ]

    return severity_score, filtered_tweets, percentage



def generate_pdf(tweets_data, keyword, output_file='output.pdf'):
    severity_score, filtered_tweets, percentage = find_severity_score(tweets_data, keyword)

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
                background-color: #333;
                color: #fff;
                font-size: 1.2em;
                position: running(header);
                width: 640px;
                border-top-left-radius: 50%; /* Upper left corner */
                border-top-right-radius: 50%; /* Upper right corner */
            }
            footer {
                text-align: center;
                padding: 10px 0;
                margin-left: -19px;
                margin-bottom: -55px;
                background-color: #333;
                color: #fff;
                font-size: 1.2em;
                position: running(footer);
                width: 640px;
                border-bottom-left-radius: 50%; /* Upper left corner */
                border-bottom-right-radius: 50%; /* Upper right corner */
                position: fixed;
                bottom: 0;
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
            {get_current_pakistan_time()}
        </footer>
    </body>
    </html>
    """

    # Convert HTML to PDF
    HTML(string=html_content).write_pdf(output_file)


# Example usage
keyword = 'israeli bombardment'
generate_pdf(tweets_data, keyword)
