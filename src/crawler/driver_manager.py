from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


class DriverManager:
    @staticmethod
    def init_driver():
        # Giả lập trình duyệt Mobile để truy cập mbasic.facebook.com
        MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36"

        # Tạo Chrome Options
        chrome_options = Options()

        # Cấu hình cửa sổ trình duyệt
        WINDOW_SIZE = "480,800"  # Kích thước mobile
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")

        # Thêm User-Agent để Facebook nhận diện là Mobile
        chrome_options.add_argument(f"user-agent={MOBILE_USER_AGENT}")

        # Các tùy chọn để Selenium chạy mượt hơn
        chrome_options_args = [
            '--no-sandbox',
            '--disable-infobars',
            '--disable-dev-shm-usage',
            '--disable-notifications',
            '--disable-blink-features=AutomationControlled',
            '--disable-popup-blocking',
            '--disable-gpu' if os.name == 'nt' else '',  # Chỉ tắt GPU trên Windows
        ]

        # Thêm các tùy chọn vào Chrome
        for arg in chrome_options_args:
            if arg:
                chrome_options.add_argument(arg)

        # Tắt Automation Extension để Selenium giống người dùng hơn
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Giảm tải hình ảnh và script để load nhanh hơn
        prefs = {
            "profile.default_content_setting_values.notifications": 2,  # Tắt thông báo
            "profile.managed_default_content_settings.images": 2,  # Không tải ảnh
            "profile.managed_default_content_settings.javascript": 1,  # Vẫn chạy JS
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Khởi tạo WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        return driver
