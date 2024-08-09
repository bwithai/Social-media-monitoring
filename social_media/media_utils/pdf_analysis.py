import pprint
import re
import time

from weasyprint import HTML
import unidecode

from social_media.media_utils.analysis import generate_pdf
from social_media.media_utils.pdf_utils import find_severity_score_based_on_post_data
from utils import get_current_pakistan_time

data = {
    'tweets': [
        {
            'original_description': 'Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M',
            'images': ['https://pbs.twimg.com/media/GT_Ot1uXQAA_gW0?format=jpg&name=small',
                       'https://pbs.twimg.com/media/GUD1DkNWgAAFMfV?format=png&name=small',
                       'https://pbs.twimg.com/media/GT6DH3iWAAA6SFo?format=jpg&name=small'],
            'links': ['https://example.com', 'https://anotherexample.com']
        },
        {
            'original_description': 'Muhammad Jalal reposted\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436\n11K\n14K\n310K',
            'images': ['https://pbs.twimg.com/media/GT6DH3iWAAA6SFo?format=jpg&name=small'],
            'links': []
        },
        {
            'original_description': 'Muhammad Jalal\n@jalalayn\n·\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\nNour Naim| نُور\n@NourNaim88\n·\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n5\n80\n299\n5.9K',
            'images': [],
            'links': ['https://example.com']
        }
    ],
    'fb_posts': [
        {
            'original_description': 'John Doe\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244 likes\n3.2K comments',
            'images': ['https://via.placeholder.com/150'],
            'links': ['https://example.com']
        },
        {
            'original_description': 'Jane Smith\nJul 30\nThis is not a movie scene\n\nA child in #Gaza carries his father’s injured leg while fleeing heavy Israeli bombardment in the Khan Younis area, southern #Gaza Strip.\n436 likes\n11K comments',
            'images': ['https://via.placeholder.com/150', 'https://via.placeholder.com/200'],
            'links': ['https://anotherexample.com']
        },
        {
            'original_description': 'John Doe\n8h\nأَلَآ إِنَّ نَصْرَ ٱللَّهِ قَرِيبٌۭ\nUnquestionably, the help of Allāh is near.\n5 likes\n80 comments',
            'images': [],
            'links': []
        }
    ]
}

# replayce with actual post data
keyword = 'israeli bombardment'
categories_keywords = {
    'religious': ['Allāh', 'Islam', 'pray', 'faith', 'spiritual', 'mosque', 'Quran'],
    'political': ['bombardment', 'Gaza', 'liberalism', 'racism', 'superiority', 'election', 'democracy'],
    'open_minded': ['tolerance', 'diversity', 'equality', 'freedom', 'inclusivity', 'acceptance'],
    'technology': ['AI', 'blockchain', 'cybersecurity', 'innovation', 'programming'],
    'health': ['wellness', 'nutrition', 'exercise', 'mental health', 'therapy']
}
generate_pdf(data, categories_keywords, 'new_analysis.pdf')
# time.sleep(3)
# pprint.pprint(data)
