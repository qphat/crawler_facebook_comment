import time
from selenium.common import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


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
                    if (len(new_cookie[1].split("|"))):
                        new_cookie[1] = new_cookie[1].split("|")[0]
                    if (";" not in new_cookie[1]):
                        new_cookie[1] = new_cookie[1] + ";"

            conv = new_cookie[0] + " " + new_cookie[1]
            if (conv.split(" ")[0] == "c_user="):
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

    def crawl_comments(self, url, csv_file_path):
        self.driver.get(url)

        # # Click vào nút bình luận
        # WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, ""))).click()
        #
        # # Chờ nút "Phù hợp nhất" xuất hiện và click vào
        # WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "(//span[contains(text(),'Phù hợp nhất')])[1]"))).click()

        # Chờ nút lựa chọn hiển thị tất cả bình luận xuất hiện và click vào
        # WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "(//div[@role='menuitem'])[3]"))).click()

        # Chờ đợi và click vào nút "Xem thêm bình luận" khoảng 50 lần
        for i in range(100):
            try:
                # Tìm thẻ span chứa text "Xem thêm bình luận"
                show_more_comments_span = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[contains(text(), 'Xem thêm bình luận')]/ancestor::div[1]"))
                )
                self.driver.execute_script('arguments[0].click();', show_more_comments_span)

                # Đợi một chút để bình luận mới được tải xong
                print(f'Have shown more comments {i + 1} times')
                time.sleep(2)
            except TimeoutException:
                print("Không tìm thấy nút 'Xem thêm bình luận' hoặc đã đạt tới số lượng bình luận tối đa.")
                break

        # Cập nhật lại comments_container sau khi đã hiển thị thêm bình luận
        x_path = "/html/body/div[1]/div/div/div[1]/div/div[3]/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div[2]/div[3]/div[1]/div[2]"
        comments_container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, x_path)))

        comments = self.driver.execute_script("""
            function getTextFromNode(node) {
                let text = "";

                if (!["A", "BUTTON"].includes(node.tagName) && !(node.tagName === "DIV" && node.getAttribute("role") === "button")) {
                    node.childNodes.forEach(child => {
                        if (child.nodeType === 3) { // Node.TEXT_NODE
                            text += child.nodeValue;
                        } else if (child.nodeType === 1) { // Node.ELEMENT_NODE
                            text += getTextFromNode(child);
                        }
                    });
                }
                return text;
            }
            const commentNodes = arguments[0].childNodes;
            const comments = [];
            Array.from(commentNodes).forEach(node => {
                const commentText = getTextFromNode(node);
                if (commentText.trim() !== "")
                    comments.push(commentText);
            });

            return comments;
        """, comments_container)

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for comment in comments:
                writer.writerow([comment])