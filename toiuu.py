import re
import sys
import time

from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class FacebookClient:
    def __init__(self, driver, cookie):
        self.driver = driver
        self.cookie = cookie

    def convertToCookie(self):
        try:
            new_cookie = ["c_user=", "xs="]
            cookie_arr = self.cookie.split(";")
            for i in cookie_arr:
                if i.__contains__('c_user='):
                    new_cookie[0] = new_cookie[0] + (i.strip() + ";").split("c_user=")[1]
                if i.__contains__('xs='):
                    new_cookie[1] = new_cookie[1] + (i.strip() + ";").split("xs=")[1]
                    if len(new_cookie[1].split("|")):
                        new_cookie[1] = new_cookie[1].split("|")[0]
                    if ";" not in new_cookie[1]:
                        new_cookie[1] = new_cookie[1] + ";"

            conv = new_cookie[0] + " " + new_cookie[1]
            if conv.split(" ")[0] == "c_user=":
                return
            else:
                return conv
        except:
            print("Error Convert Cookie")

    def loginFacebookByCookie(self):
        try:
            cookie = self.convertToCookie()
            if cookie is not None:
                script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("' + cookie + '"); location.href = "https://mbasic.facebook.com"; })();'
                self.driver.execute_script(script)
                time.sleep(5)
        except:
            print("Error Login Facebook By Cookie")

    def login_by_cookie(self):
        try:
            self.driver.get('https://mbasic.facebook.com/')
            time.sleep(2)
            self.loginFacebookByCookie()

            return True
        except:
            print("check live fail")

    def scroll_incrementally(self):
        scroll_pause_time = 3  # Thời gian chờ giữa các lần cuộn
        max_scroll_attempts = 50  # Giới hạn số lần cuộn để tránh vòng lặp vô hạn
        scroll_step = 1000  # Cuộn từng bước 1000px

        for _ in range(max_scroll_attempts):
            # Cuộn từng bước
            self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_step)
            time.sleep(scroll_pause_time)

            # Kiểm tra xem có nội dung mới không
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            current_position = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
            if current_position >= new_height:
                # Đã đến cuối trang, kiểm tra thêm 2 lần nữa để chắc chắn
                for _ in range(2):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(scroll_pause_time)
                    if self.driver.execute_script("return document.body.scrollHeight") == new_height:
                        print("Đã cuộn đến cuối trang, không còn nội dung mới.")
                        return
                break

    def expand_comments(self):
        buttons_xpath = [
            "//span[contains(text(), 'Hiển thị bình luận trước')]",
            "//span[contains(text(), 'Xem thêm')]",
            "//span[contains(text(), 'Xem bình luận trước đó')]",
            "//span[contains(text(), 'Xem thêm trả lời')]"
        ]
        for xpath in buttons_xpath:
            while True:
                try:
                    buttons = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.XPATH, xpath))
                    )
                    for button in buttons:
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                            self.driver.execute_script("arguments[0].click();", button)
                            time.sleep(2)
                        except Exception:
                            continue
                    print(f"Đã nhấp vào các nút {xpath}")
                except TimeoutException:
                    print(f"Không còn nút {xpath} để nhấp.")
                    break

    def crawl_comments(self, url):
        self.driver.get(url)
        time.sleep(5)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Mở rộng tất cả bình luận
        self.expand_comments()

        # Cuộn trang từ từ để tải nội dung
        self.scroll_incrementally()

        # XPath chọn container bình luận
        comment_xpath = "//div[@data-mcomponent='MContainer' and .//img and count(.//div[@class='native-text']) >= 2]"
        try:
            comment_containers = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, comment_xpath))
            )
        except TimeoutException:
            print("Không tìm thấy bình luận.")
            return []

        print(f"Tìm thấy {len(comment_containers)} container bình luận")
        comments_data = set()

        extract_text_script = """
            function getTextFromNode(node) {
                let text = "";
                if (!["A", "BUTTON"].includes(node.tagName) && !(node.tagName === "DIV" && node.getAttribute("role") === "button")) {
                    node.childNodes.forEach(child => {
                        if (child.nodeType === 3) text += child.nodeValue;
                        else if (child.nodeType === 1) text += getTextFromNode(child);
                    });
                }
                return text;
            }
            return Array.from(arguments[0].querySelectorAll('div.native-text')).map(node => getTextFromNode(node)).filter(text => text.trim() !== "");
        """

        def is_valid_text(text):
            return len(text.strip()) > 1 and not re.match(r'\d+\s*(giờ|phút)?$', text) and text.strip() not in [
                "Thích", "Phản hồi", "·", "Theo dõi"]

        for container in comment_containers:
            try:
                texts = self.driver.execute_script(extract_text_script, container)
                print(f"Dữ liệu thô từ container: {texts}")
                if len(texts) >= 2:
                    username, comment_content = None, None
                    for i, text in enumerate(texts):
                        if is_valid_text(text):
                            username = text.strip()
                            for j in range(i + 1, len(texts)):
                                if is_valid_text(texts[j]):
                                    comment_content = texts[j].strip()
                                    break
                            break
                    if username and comment_content:
                        comment_content = re.sub(r'[\U000f0000-\U000fFFFF]', '', comment_content)
                        comments_data.add((username, comment_content))
            except StaleElementReferenceException:
                print("Phần tử bị mất, bỏ qua container này.")
                continue
            except Exception as e:
                print(f"Lỗi khi xử lý container: {str(e)}", file=sys.stderr)
                continue

        comments_data = [{"username": u, "comment": c} for u, c in comments_data]
        for data in comments_data:
            print(f"Người bình luận: {data['username']}")
            print(f"Nội dung: {data['comment']}")
            print("-" * 50)
        return comments_data






