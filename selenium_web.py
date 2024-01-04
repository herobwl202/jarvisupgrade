# selenium_web.py
import pyttsx3 as p
from selenium import webdriver
from selenium.webdriver.common.by import By

class infow():
    def __init__(self):
        self.driver = webdriver.Firefox()

    def get_info(self, query):
        self.query = query
        self.driver.get("https://www.wikipedia.org")
        
        # Sử dụng mô-đun By để tìm phần tử bằng XPath
        search = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')
        search.click()
        search.send_keys(query)
        
        # Tìm phần tử nút "Search" bằng XPath
        enter = self.driver.find_element(By.XPATH, '/html/body/div[3]/form/fieldset/button')
        enter.click()

        # Tìm đoạn văn bản bạn muốn đọc bằng XPath
        # Ví dụ: lấy nội dung của đoạn văn bản đầu tiên trong kết quả tìm kiếm
        result = self.driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/p[2]')
        text_to_read = result.text
        
        return text_to_read

# Khởi tạo và sử dụng hệ thống đọc tiếng nói (speech synthesis)
engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Hàm để hệ thống đọc văn bản
def speak(text):
    engine.say(text)
    engine.runAndWait()