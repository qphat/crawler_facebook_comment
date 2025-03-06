
import re

import pandas as pd

from src.cleaner.CSVHandler import CSVHandler
from src.crawler.driver_manager import DriverManager
from src.crawler.facebook_client import FacebookClient
from src.config import FACEBOOK_COOKIE, post_url
from src.cleaner import basic_cleaner


def main():
    # 1. Khởi tạo trình duyệt
    driver = DriverManager.init_driver()
    try:
        # 2. Đăng nhập Facebook bằng cookie
        facebook_client = FacebookClient(driver, FACEBOOK_COOKIE)
        facebook_client.login_by_cookie()

        # 3. Crawl bình luận từ bài viết
        # comments = facebook_client.crawl_comments(post_url)
        comment = facebook_client.crawl_comments_with_ids(post_url)
        print(comment)

        # def extract_group_post_id(post_url):
        #     match = re.search(r'groups/(\d+)/posts/(\d+)', post_url)
        #     if match:
        #         return match.group(1), match.group(2)
        #     return None, None
        #
        # group_id, post_id = extract_group_post_id(post_url)
        # print(f"group_id: {group_id}, post_id: {post_id}")
        #
        # group_id, post_id = extract_group_post_id(post_url)
        #
        # # 4. Khởi tạo CSVHandler và lưu dữ liệu thô
        # csv_handler = CSVHandler(group_id, post_id)
        # csv_handler.save_raw_comments(comments)
        #
        # # 5. Làm sạch dữ liệu
        # df = pd.read_csv(csv_handler.filename, encoding='utf-16')
        # cleaner = basic_cleaner
        # cleaner.apply_cleaning()
        # cleaned_df = cleaner.get_cleaned_data()
        #
        # # 6. Lưu dữ liệu đã làm sạch
        # csv_handler.save_cleaned_comments(cleaned_df)

    except Exception as e:
        print(f"Lỗi: {e}")

    finally:
        # 7. Đóng trình duyệt
        driver.quit()


if __name__ == "__main__":
    main()
