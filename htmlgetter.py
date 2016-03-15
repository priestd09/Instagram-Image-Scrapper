import selenium.webdriver as webdriver
import time
import random
from time import sleep


def get_html(url, scroll_time):
    driver = webdriver.Firefox()
    driver.get(url)

    old_time = int(round(time.time() * 1000))
    while (int(round(time.time() * 1000)) - old_time) < scroll_time*1000:
        random.seed()
        n = random.random()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-"+str(int(n*150))+");")
        sleep(0.5)

    page_source = driver.page_source
    driver.close()
    return page_source
