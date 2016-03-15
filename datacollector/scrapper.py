import threading
import Queue
import time
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
import urllib
import os


class Scrapper(threading.Thread):
    def __init__(self, thread_id, instagram_url, hashtag, links, queue_lock, work_queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.instagram_url = instagram_url
        self.hashtag = hashtag
        self.links = links
        self.queue_lock = queue_lock
        self.work_queue = work_queue

    def run(self):
        print "Starting scrapper id: " + str(self.thread_id) + ", Links to proceed: " + str(len(self.links)) + "\n"
        self.analyse()
        print "Exiting scrapper id: " + str(self.thread_id) + "\n"

    def analyse(self):
        directory = self.hashtag+"/"+"Images/"
        driver = webdriver.Firefox()
        for link in self.links:
            driver.get(link)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            y = soup.find('img',{'class':'_icyx7'})
            start_index = str(y).find('src="')
            y = str(y)[start_index+5:]
            end_index = y.find('.jpg?')
            image_source_url = y[:end_index+4]
            if image_source_url == "":
                #video
                self.queue_lock.acquire()
                self.work_queue.put("video")
                self.queue_lock.release()
                continue

            urllib.urlretrieve(image_source_url, directory+os.path.basename(image_source_url))

            y = soup.find('span', {'class':'_tf9x3'})
            start_index = str(y).find('.0.1.0.0.0.2.0.0.0.1">')
            y = str(y)[start_index+22:]
            end_index = y.find('<')
            number_of_likes = y[:end_index]

            hashtags_list = []
            y = soup.find('li', {'class':'_nk46a'})
            y = str(y)
            while (y.find('#') != -1):
                start_index = y.find('#')
                y = y[start_index+1:]
                end_index = y.find('</a>')
                hashtags_list.append(y[:end_index])

            #Retrieving followers number from user
            z = soup.find('div', {'class':'_f95g7'})
            start_index = str(z).find('href="')
            z = str(z)[start_index+6:]
            end_index = z.find('"')
            user_url = z[:end_index]
            user_url = self.instagram_url + user_url

            driver.get(user_url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            f = soup.find('span', {'class':'_pr3wx'})
            start_index = str(f).find('title="')
            f = str(f)[start_index+7:]
            end_index = f.find('"')
            followers = f[:end_index]

            self.queue_lock.acquire()
            self.work_queue.put([os.path.basename(image_source_url), number_of_likes, followers, hashtags_list])
            self.queue_lock.release()
        driver.close()
