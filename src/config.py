from dotenv import load_dotenv
import os

load_dotenv()

FACEBOOK_COOKIE = os.getenv("FACEBOOK_COOKIE")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DEFAULT = "mysql_default"

post_url = "https://www.facebook.com/watch/?v=1275155160285835"
output_crawl_file = "data/comments.csv"
output_clean_file = "data/cleaned_comments.csv"