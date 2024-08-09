import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import unidecode
import io
import base64

PER_PAGE_HEADER_FOOTER = """header {
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
            }"""


def find_severity_score_based_on_post_data(data, keyword):
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
    for tweet in data['tweets']:
        tweet_text = tweet['original_description']
        if keyword_pattern.search(unidecode.unidecode(tweet_text).lower()):
            tweet['original_description'] = keyword_pattern.sub(highlight_match, tweet_text)
            severity_score += 1

    for post in data['fb_posts']:
        post_text = post['original_description']
        if keyword_pattern.search(unidecode.unidecode(post_text).lower()):
            post['original_description'] = keyword_pattern.sub(highlight_match, post_text)
            severity_score += 1

    # Calculate the percentage
    percentage = round((severity_score / len(data['tweets'])) * 100, 2)

    # Collect filtered tweets for output
    filtered_description = [
        tweet['original_description'] for tweet in data['tweets']
        if highlighted_keyword in tweet['original_description']
    ]

    return severity_score, filtered_description, percentage


def find_severity_score(data, keywords):
    results = []

    for keyword in keywords:
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
        for tweet in data['tweets']:
            tweet_text = tweet['original_tweet_text']
            if keyword_pattern.search(unidecode.unidecode(tweet_text).lower()):
                tweet['original_tweet_text'] = keyword_pattern.sub(highlight_match, tweet_text)
                severity_score += 1

        # Calculate the percentage
        percentage = round((severity_score / len(data['tweets'])) * 100, 2)

        # Collect filtered tweets for output
        filtered_tweets = [
            tweet['original_tweet_text'] for tweet in data['tweets']
            if highlighted_keyword in tweet['original_tweet_text']
        ]

        results.append({
            'keyword': keyword,
            'severity_score': severity_score,
            'percentage': percentage,
            'filtered_tweets': filtered_tweets
        })

    return results


def analyse_severity(data, categories_keywords):
    def count_and_highlight_keywords(text, keywords):
        # Normalize the text to lower case for case-insensitive matching
        text_lower = text.lower()
        # Count occurrences of each keyword and highlight them
        keyword_counts = Counter()
        for keyword in keywords:
            normalized_keyword = keyword.lower()
            keyword_pattern = re.compile(re.escape(normalized_keyword), re.IGNORECASE)
            matches = keyword_pattern.findall(text_lower)
            keyword_counts[keyword] = len(matches)
            text = keyword_pattern.sub(lambda match: f"<span style='color:blue;'>{match.group(0)}</span>", text)
        return keyword_counts, text

    # Aggregate counts and highlighted texts for all categories
    category_counts = {category: Counter() for category in categories_keywords}
    highlighted_tweets = []

    if 'tweets' in data:
        for tweet in data['tweets']:
            tweet_text = tweet['original_description']
            highlighted_text = tweet_text
            for category, keywords in categories_keywords.items():
                counts, highlighted_text = count_and_highlight_keywords(highlighted_text, keywords)
                category_counts[category].update(counts)
                tweet['original_description'] = highlighted_text
            highlighted_tweets.append(highlighted_text)

    if 'fb_posts' in data:
        for post in data['fb_posts']:
            post_text = post['original_description']
            highlighted_text = post_text
            for category, keywords in categories_keywords.items():
                counts, highlighted_text = count_and_highlight_keywords(highlighted_text, keywords)
                category_counts[category].update(counts)
                post['original_description'] = highlighted_text
            highlighted_tweets.append(highlighted_text)

    # Calculate unique keyword matches and category scores
    category_scores = {
        category: {
            'matched': sum(1 for count in keyword_counts.values() if count > 0),
            'len': len(keyword_counts),
            'counter': Counter({k: v for k, v in keyword_counts.items() if v > 0})
        }
        for category, keyword_counts in category_counts.items()
    }

    return category_scores


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
