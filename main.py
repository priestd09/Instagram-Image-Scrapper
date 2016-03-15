import sys
import data_structure as ds
import datapreparer.htmlgetter as html
import datacollector.scrapper as scrapper
from bs4 import BeautifulSoup
import splitter
import threading
import Queue
import time

instagram_url = "http://instagram.com"
hashtag_suffix = "/explore/tags/"

if len(sys.argv) != 4:
    print "Wrong number of arguments"
    print "script.py <hashtag> <number of collectors> <number of seconds to scroll down>"
    sys.exit(1)

hashtag = str(sys.argv[1])
number_of_collectors = int(sys.argv[2])
scrolling_time = int(sys.argv[3])
#hashtag = "e46"
#scrolling_time = 10

ds.Dir.create_directory(hashtag)
directory = hashtag+"/"+"Images/"
ds.Dir.create_directory(directory)
analysed_images = ds.File.load_info_from_json_file(hashtag)

html_code = html.get_html(instagram_url+hashtag_suffix+hashtag+'/', scrolling_time)
soup = BeautifulSoup(html_code, "html.parser")
html_image_a_elements = soup.findAll('a', {'class':'_8mlbc _t5r8b'})
image_links = []
for x in html_image_a_elements:
    startIndex = str(x).find('href=')
    x = str(x)[startIndex+6:]
    endIndex = x.find('"')
    image_links.append(instagram_url + x[:endIndex])

print "Number of links to proceed: " + str(len(image_links))
if len(image_links)/4 < number_of_collectors:
    number_of_collectors = len(image_links)/4
if number_of_collectors < 1:
    number_of_collectors = 1

links_to_proceed = splitter.list_splitter(image_links, number_of_collectors)

queue_lock = threading.Lock()
work_queue = Queue.Queue(20)
threads = []
thread_id = 1
for links in links_to_proceed:
    thread = scrapper.Scrapper(thread_id, instagram_url, hashtag, links, queue_lock, work_queue)
    thread.start()
    threads.append(thread)
    thread_id += 1

image_info = []
empty_queue = True
videos = 0
start_time = int(round(time.time()))
time_list = []
stop = False

while True:
    current_time = int(round(time.time()))
    time_list.append([current_time, len(image_info)+videos])
    period = 10
    if len(time_list) > period:
        new_time_list = []
        for i in reversed(range(period)):
            last_index = len(time_list) - 1
            new_time_list.append(time_list[last_index - i])
        time_list = new_time_list

    if threading.activeCount() == 1:
        stop = True
    queue_lock.acquire()
    if not work_queue.empty():
        empty_queue = False
        image = 0
        while not work_queue.empty():
            element = work_queue.get()
            if element == "video":
                videos += 1
            else:
                image += 1
                image_info.append(element)
        if image == 0:
            empty_queue = True
    queue_lock.release()
    if not empty_queue:
        ds.File.save_data_as_json(hashtag+"/"+"imagesInfo.json", image_info)
        avg_time_delta = (current_time - start_time)/float(60)
        avg_speed_per_min = (len(image_info)+videos)/avg_time_delta
        time_delta = (time_list[0][0] - time_list[len(time_list)-1][0])/float(60)
        images_analysed_delta = time_list[0][1] - time_list[len(time_list)-1][1]
        speed_per_min = images_analysed_delta/time_delta
        print "Analysed: " + str(len(image_info) + videos) + ", avg speed: " + str("%.2f" % avg_speed_per_min) + " /min" + ", speed: " + str("%.2f" % speed_per_min) + " /min"

    if stop:
        break
    empty_queue = True
    time.sleep(5)

print "Analysed: " + str(len(image_info) + videos) + "links."
print "Retrieved: " + str(len(image_info)) + "images."
print "Number of skipped videos: " + str(videos)
print "Exiting Main Thread"
