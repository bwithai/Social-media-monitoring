import pprint
import re

from weasyprint import HTML
import unidecode

from social_media.media_utils.analysis import generate_pdf
from social_media.media_utils.pdf_utils import find_severity_score_based_on_post_data
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
            'original_tweet_text': 'Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M'
        },
        {
            'original_tweet_text': 'Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M'
        },
        {
            'original_tweet_text': 'Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M'
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

# replayce with actual post data
keyword = 'israeli bombardment'
generate_pdf(tweets_data, keyword)
