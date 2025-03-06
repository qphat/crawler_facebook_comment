from dotenv import load_dotenv
import os

load_dotenv()

FACEBOOK_COOKIE = os.getenv("FACEBOOK_COOKIE")

post_url = "https://www.facebook.com/groups/1753958561470479/posts/2686282218238104?locale=vi_VN"
output_crawl_file = "data/comments.csv"
output_clean_file = "data/cleaned_comments.csv"