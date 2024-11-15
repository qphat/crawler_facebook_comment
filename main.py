from crawler.config import FACEBOOK_COOKIE
from crawler.driver_manager import DriverManager
from crawler.facebook_client import FacebookClient


def crawl_facebook_comments():
    driver = DriverManager.init_driver()
    fb_client = FacebookClient(driver, FACEBOOK_COOKIE)

    # Login và crawl dữ liệu
    fb_client.login_by_cookie()
    fb_client.crawl_comments(
        url="https://www.facebook.com/watch/?v=1275155160285835",
        csv_file_path="/path/to/data/comments.csv"
    )
    driver.quit()
