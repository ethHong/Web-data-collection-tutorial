from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import platform
from langdetect import detect
import json
from tqdm import tqdm

# If browser is loading too fast, enable time.sleep option
# import time

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Choose right chromedriver of your OS

if platform.system() == "Windows":
    driverpath = os.getcwd() + "/chromedriver.exe"
else:
    driverpath = os.getcwd() + "/chromedriver"


def get_links(page, lang=True):

    url = "https://www.coursera.org/directory/courses?page=" + str(page)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    links = soup.findAll("a", {"class": "c-directory-link"}, href=True)

    course_name = []
    course_links = []
    for i in links:
        if detect(i.text) == "en":
            course_name.append(i.text)
            course_links.append("https://coursera.org" + i["href"])

    collected = {}
    for i in range(0, len(course_name)):
        collected[course_name[i]] = course_links[i]
    return collected


def crawl(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    result = {}

    try:
        if soup.findAll("div", {"class": "_jyhj5r SyllabusWeek"}) != []:
            syllabus_weeks = soup.findAll("div", {"class": "_jyhj5r SyllabusWeek"})

            result = {}
            for i in range(0, len(syllabus_weeks)):
                week = "Week_{}".format(i + 1)
                result[week] = {}
                syllabus = syllabus_weeks[i]
                titles = syllabus.findAll("h2", {"class": "headline-2-text bold m-b-2"})
                contents = syllabus.findAll("p")
                for t in range(0, len(titles)):
                    result[week]["Title_{}".format(t + 1)] = titles[t].text
                    result[week]["Contents_{}".format(t + 1)] = contents[t].text
        else:
            result = "None"

    except:
        result = "None"

    return result


driver = webdriver.Chrome(driverpath, chrome_options=options)
data = {}

start = input("Which page to start?: ")
page = input("How many pages to crawl? (Max 194...): ")

for i in range(int(start), int(page) + 1):

    print("Start scraping...")

    links = get_links(i, lang=True)  # Detect language, and if not English, skip
    names = list(links.keys())

    for c in tqdm(range(0, len(names))):
        course = names[c]
        link = links[course]
        data[course] = crawl(link)

    if i % 10 == 0:
        print("Page {} out of {}...".format(i, page))
        # backup:

        with open(
            "backup/coursera_syllabus_backup{}.json".format(start),
            "w",
            encoding="utf-8",
        ) as json_file:
            json.dump(data, json_file)
        print("Saved backup")

# Save as json file
with open("output/coursera_syllabus_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file)
