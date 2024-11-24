from airflow.models import BaseOperator
from src.config import FACEBOOK_COOKIE
from src.crawler.driver_manager import DriverManager
from src.crawler.facebook_client import FacebookClient
import csv

class CrawlCommentsOperator(BaseOperator):
    def __init__(self, post_url, output_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_url = post_url
        self.output_file = output_file

    def execute(self, context):
        driver = DriverManager.init_driver()
        crawler = FacebookClient(driver, FACEBOOK_COOKIE)
        crawler.login_by_cookie()
        comments = crawler.crawl_comments(
            url=self.post_url
        )
        driver.quit()
        with open(self.output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["comment"])
            for comment in comments:
                writer.writerow([comment])
