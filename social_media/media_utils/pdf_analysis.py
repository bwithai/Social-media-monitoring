from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import io
import requests

from database.queries import get_user_by_id_extend_posts


def fetch_image(url):
    response = requests.get(url)
    img = io.BytesIO(response.content)
    return img


# Sample dictionary
data = {
    "_id": "66a73f4395588192845dc5b6",
    "name": "zain",
    "email": "test@gmail.com",
    "mobile_number": "0303-3439433",
    "address": "sdfdsfs",
    "fb_username": "agha.rameez.3",
    "insta_username": None,
    "x_username": "jalalayn",
    "num_fb_posts": 10,
    "num_insta_posts": 0,
    "num_x_days": 10,
    "crawler": {
        "X": [
            {
                "original_tweet_text": "Pinned\nMuhammad Jalal\n@jalalayn\n·\nDec 19, 2022\nThere are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world.\n244\n3.2K\n11K\n1M",
                "tweet": {
                    "engagement": {
                        "replays": "244",
                        "retweets": "3.2K",
                        "likes": "11K",
                        "views": "1M"
                    },
                    "context": "tweeted by Pinned",
                    "datetime_on_x": "·",
                    "username": "Muhammad Jalal",
                    "tweet_text": "There are two kinds of bigotry in the west. A visceral racism that targets people of colour and a ‘sophisticated’ liberalism that masks hatred behind a facade of tolerance. Both come from a misplaced superiority. A belief that European man and his culture are a gift to the world."
                },
                "images": [
                    "https://pbs.twimg.com/profile_images/1760045875622236161/3TFGsXIX_normal.jpg",
                    "https://pbs.twimg.com/media/FkWwpC2XwAEYWDV?format=jpg&name=small"
                ],
                "videos": [],
                "date": "2022-12-19 16:55:51",
                "hashtags": [
                    "palestine_genocide"
                ],
                "links": [],
                "reposted": "no",
                "pinned": "yes"
            },
            {
                "original_tweet_text": "Muhammad Jalal reposted\nThe Holy Quran\n@AlMosahfEN\n·\n3h\nوَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مِنْ أَمْرِهِ يُسْرًا\n\nand for those who fear Allah, He will make their path easy.\n12\n55\n2.1K",
                "tweet": {
                    "engagement": {
                        "replays": None,
                        "retweets": "12",
                        "likes": "55",
                        "views": "2.1K"
                    },
                    "context": "Muhammad Jalal reposted tweet of The Holy Quran",
                    "datetime_on_x": "3h",
                    "username": "@AlMosahfEN",
                    "tweet_text": "وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مِنْ أَمْرِهِ يُسْرًا\n"
                },
                "images": [
                    "https://pbs.twimg.com/profile_images/871766315106742273/-C_wgtEP_normal.jpg"
                ],
                "videos": [],
                "date": "2024-07-29 03:26:00",
                "hashtags": [],
                "links": [],
                "reposted": "yes",
                "pinned": "no"
            }
        ],
        "facebook": [
            {
                "original_description": "Agha Rameez Haidery\no\nd\nS\nt\ne\ns\nr\no\np\nn\nf\nh\n9\nm\nl\n6\nu\nl\n3\nu\n0\n9\n9\nt\nu\n1\n5\nm\ni\ng\nt\ng\nm\n6\ng\n9\nh\n1\nu\nf\n7\n9\nf\nh\n1\nc\ng\n3\nf\n1\n2\ni\n8\nl\n2\n1\nf\n0\n4\n8\n  ·\nمیدان اب سج چکا ہے\n سب اختلافات ایک سایئڈ پررکھیۓ اور جماعت اسلامی کا ساتھ دیجئے ورنہ مزید مہنگائی کے طوفان کا انتظار کریں\nSee translation\nAll reactions:\n43\n43\n2 comments\n21 shares\nLike\nComment\nSend\nShare\nView more comments\nMian Farhan\n9 h\n9 hours ago\nLike\nReply\n\nComment as Abiha Khan",
                "clean_description": {
                    "post_text": "میدان اب سج چکا ہے سب اختلافات ایک سایئڈ پررکھیۓ اور جماعت اسلامی کا ساتھ دیجئے ورنہ مزید مہنگائی کے طوفان کا انتظار کریںSee translation",
                    "engagement": {
                        "likes": "43 likes",
                        "comments": "2 comments",
                        "shares": "21 shares"
                    },
                    "display_comment": "Mian Farhan commented at 9 h9 hours ago comment contain emoji"
                },
                "hashtags": [
                    "#dreamers",
                    "#fight"
                ],
                "datetime": None,
                "links": [],
                "images": [
                    "https://scontent-ams4-1.xx.fbcdn.net/v/t39.30808-6/453042938_8882607491765578_253225785514062935_n.jpg?stp=dst-jpg_p526x395&_nc_cat=101&ccb=1-7&_nc_sid=833d8c&_nc_ohc=11KCvCtUFq0Q7kNvgEH2xDY&_nc_ht=scontent-ams4-1.xx&oh=00_AYCB-hm1X1rDG51xhhz5zYgzfKCSytRWyrP95ARK4ayetg&oe=66AD1ACA",
                    "https://scontent-ams4-1.xx.fbcdn.net/v/t39.30808-6/453478735_8882607735098887_8133629711487230620_n.jpg?stp=dst-jpg_s600x600&_nc_cat=101&ccb=1-7&_nc_sid=833d8c&_nc_ohc=qCAYPB-6F64Q7kNvgF-XNXE&_nc_ht=scontent-ams4-1.xx&oh=00_AYBYlfO-mrW36eijrFsPu6hD2gisWT6XV7xNb7WJKUiSrQ&oe=66AD027E",
                    "https://scontent-ams2-1.xx.fbcdn.net/v/t39.30808-6/453156315_8882614321764895_6596108640383355659_n.jpg?stp=dst-jpg_s600x600&_nc_cat=110&ccb=1-7&_nc_sid=833d8c&_nc_ohc=0WiWyBT44KAQ7kNvgH8uDCo&_nc_ht=scontent-ams2-1.xx&oh=00_AYCQEaDzDHjiOaPB7hLwTKf-mQOihTqECWbzNJLZFLHkoQ&oe=66AD058B",
                    "https://scontent-ams2-1.xx.fbcdn.net/v/t39.30808-6/452052499_497159832858646_4190593158861826150_n.jpg?stp=dst-jpg_p75x225&_nc_cat=104&ccb=1-7&_nc_sid=bd9a62&_nc_ohc=VLg-wkFSKL8Q7kNvgG2RJNf&_nc_ht=scontent-ams2-1.xx&oh=00_AYCMSanzg8hSIN-PsXTeAmqGoziailgLgnM8qds167PiUg&oe=66AD1E35"
                ]
            },
            {
                "original_description": "Agha Rameez Haidery\n  ·\nجماعت اسلامی نے بجلی بل کے خلاف دھرنا دیا ہے۔ میں ذاتی طور پر سمجھتا ہوں کہ یہ پوری قوم کا مشترکہ مسئلہ ہے پوری قوم کو اس پر یکجا ہونا چاہئے ۔ بلا تفریق مذہب و ملت اور سیاست ہمیں اپنے حق کے لیے اٹھنا چاہئے اور جماعت اسلامی کے احتجاج کو سپورٹ کرنا چاہیے\nSee translation\nAll reactions:\n1\n1\n1 share\nLike\nComment\nSend\nShare\n\nComment as Abiha Khan",
                "clean_description": {
                    "post_text": "جماعت اسلامی نے بجلی بل کے خلاف دھرنا دیا ہے۔ میں ذاتی طور پر سمجھتا ہوں کہ یہ پوری قوم کا مشترکہ مسئلہ ہے پوری قوم کو اس پر یکجا ہونا چاہئے ۔ بلا تفریق مذہب و ملت اور سیاست ہمیں اپنے حق کے لیے اٹھنا چاہئے اور جماعت اسلامی کے احتجاج کو سپورٹ کرنا چاہیےSee translation",
                    "engagement": {
                        "likes": "1 likes",
                        "comments": "",
                        "shares": ""
                    }
                },
                "hashtags": [],
                "datetime": None,
                "links": [],
                "images": []
            },
            {
                "original_description": "Agha Rameez Haidery is with Muhammad Mohsin and\n66 others\n.\n  ·\n3 مرلہ, 4 مرلہ اور 5 مرلہ کے محدود مکان آسان اقساط پر\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \nجی ٹی روڈ سے 30 سیکنڈ \n\"مراڑیاں_شریف'\nگجرات کا پہلا پروجیکٹ\n\"اپنا گھر\"\nآغاز سے تکمیل تک \nآسان اقساط پر\nمحدود مکان دستیاب ہیں\n20 فٹ گلہ + 14 فٹ گلی\nانویسٹرز حضرات کے لیے سنہری موقع\n30٪ ایڈوانس بکنگ\n1 سال میں قبضہ\n4 سال میں ادائیگی\nمزید تفصیلات کیے لیے دیے گئے نمبرز پر رابطہ کریں اور پیج کو فالو کر لیں شکریہ\nآغا رمیض احمد\nچیف ایگزیکیٹیو\nڈریم ورلڈ بلڈرز اینڈ مارکیٹنگ\nشاہین چوک گجرات\nمزید تفصیلات کے لیے پیج فالو کر لیں اور کال whatsapp پر رابطہ کر لیں\n03136870418 / 03444454418\nSee translation\nAll reactions:\n5\n5\n1 comment\nLike\nComment\nSend\nShare\nDukhi Panchi\n  ·\nFollow\nAdvance kitna\n2 d\n2 days ago\nLike\nReply\n\nComment as Abiha Khan",
                "clean_description": {
                    "post_text": "",
                    "engagement": {
                        "likes": "5 likes",
                        "comments": "1 comment",
                        "shares": ""
                    },
                    "display_comment": "Dukhi Panchi commented at 2 d2 days ago    ·FollowAdvance kitna"
                },
                "hashtags": [
                    "#FightInStreet"
                ],
                "datetime": None,
                "links": [],
                "images": [
                    "https://scontent-ams2-1.xx.fbcdn.net/v/t39.30808-6/453243199_8873291316030529_6509926813196814095_n.jpg?stp=dst-jpg_s720x720&_nc_cat=106&ccb=1-7&_nc_sid=833d8c&_nc_ohc=KjpkYNP2QsAQ7kNvgFOW3hR&_nc_ht=scontent-ams2-1.xx&oh=00_AYAA3Q_7wtTdgu1shXZgXHrx_hY-BfZ7H5F0ayWvynW1rQ&oe=66AD0757"
                ]
            }
        ]
    }
}


# Create a PDF document
def create_pdf(data, filename):
    document = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        alignment=TA_CENTER,
        textColor=HexColor('#004080'),
        spaceAfter=24
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Title'],
        fontName='Helvetica',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=HexColor('#0070C0'),
        spaceAfter=14
    )

    normal_style = styles['BodyText']
    normal_style.fontName = 'Helvetica'
    normal_style.fontSize = 12
    normal_style.leading = 14
    normal_style.spaceAfter = 12

    user_body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=12,
        leading=14,
        textColor=HexColor('#333333'),
        spaceAfter=12,
        backColor=HexColor('#E0E0E0'),
        borderPadding=(5, 5, 5, 5),
        borderColor=HexColor('#004080'),
        borderWidth=1,
        borderRadius=2
    )
    # bold_style = ParagraphStyle(name="Bold", parent=normal_style, fontName="Helvetica-Bold")

    # Add data to PDF
    story.append(Paragraph("User Information", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"ID: {data['_id']}", user_body_style))
    story.append(Paragraph(f"Name: {data['name']}", user_body_style))
    story.append(Paragraph(f"Email: {data['email']}", user_body_style))
    story.append(Paragraph(f"Mobile Number: {data['mobile_number']}", user_body_style))
    story.append(Paragraph(f"Address: {data['address']}", user_body_style))
    story.append(Paragraph(f"Facebook Username: {data['fb_username']}", user_body_style))
    story.append(Paragraph(f"Instagram Username: {data['insta_username']}", user_body_style))
    story.append(Paragraph(f"X Username: {data['x_username']}", user_body_style))
    story.append(Paragraph(f"Number of Facebook Posts: {data['num_fb_posts']}", user_body_style))
    story.append(Paragraph(f"Number of Instagram Posts: {data['num_insta_posts']}", user_body_style))
    story.append(Paragraph(f"Number of X Days: {data['num_x_days']}", user_body_style))
    story.append(Spacer(1, 0.5 * inch))

    # Add X tweets data
    story.append(Paragraph("X Tweets", subtitle_style))
    for tweet in data["crawler"]["X"]:
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(f"<b>Original Tweet Text:</b> {tweet['original_tweet_text']}", normal_style))
        story.append(Paragraph(f"<b>Tweet Context:</b> {tweet['tweet']['context']}", normal_style))
        story.append(Paragraph(f"<b>Tweet Text:</b> {tweet['tweet']['tweet_text']}", normal_style))
        story.append(Paragraph(f"<b>Tweet Engagement:</b> Replays: {tweet['tweet']['engagement']['replays']}, "
                               f"Retweets: {tweet['tweet']['engagement']['retweets']}, "
                               f"Likes: {tweet['tweet']['engagement']['likes']}, "
                               f"Views: {tweet['tweet']['engagement']['views']}", normal_style))
        story.append(Spacer(1, 0.2 * inch))
        for image_url in tweet["images"]:
            img = fetch_image(image_url)
            story.append(Image(img, 2 * inch, 2 * inch))
        story.append(Spacer(1, 0.5 * inch))

    # Add Facebook posts data
    story.append(Paragraph("Facebook Posts", subtitle_style))
    for post in data["crawler"]["facebook"]:
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph(f"<b>Original Description:</b> {post['original_description']}", normal_style))
        story.append(Paragraph(f"<b>Clean Description:</b> {post['clean_description']['post_text']}", normal_style))
        story.append(Paragraph(f"<b>Engagement: Likes:</b> {post['clean_description']['engagement']['likes']}, "
                               f"Comments: {post['clean_description']['engagement']['comments']}, "
                               f"Shares: {post['clean_description']['engagement']['shares']}", normal_style))
        story.append(Spacer(1, 0.2 * inch))
        for image_url in post["images"]:
            img = fetch_image(image_url)
            story.append(Image(img, 2 * inch, 2 * inch))
        story.append(Spacer(1, 0.5 * inch))

    # Build the PDF
    document.build(story)


user = get_user_by_id_extend_posts('66a73f4395588192845dc5b6')
# Generate the PDF
create_pdf(user, "output.pdf")
