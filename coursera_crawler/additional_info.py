from bs4 import BeautifulSoup
from selenium import webdriver
import os
import platform
from langdetect import detect
import json
from tqdm import tqdm
import re

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


def crawl_add(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Export html
    with open("source/{}.html".format(url.split("/")[-1]), "w") as file:
        file.write(str(soup))

    if soup.findAll("div", {"class": "_1fpiay2"}) != []:
        enroll = soup.findAll("div", {"class": "_1fpiay2"})[0].findAll("span")[-1].text
        enroll = int(re.sub("[^0-9.]+", "", enroll))
    else:
        enroll = "None"

    if soup.findAll("div", {"class": "_bd90rg"}) != []:
        views = soup.findAll("div", {"class": "_bd90rg"})[0].findAll("span")[-1].text
        views = int(re.sub("[^0-9.]+", "", views))
    else:
        views = "None"

    if soup.findAll("div", {"class": "instructor-wrapper"}) != []:
        instructor_infos = soup.findAll("div", {"class": "instructor-wrapper"})
        instructor_information = {}
        for i in instructor_infos:
            instructor_info = i
            instructor_name = instructor_info.find("h3").text
            instructor_title = instructor_info.find(
                "span", {"class": "instructor-title"}
            ).text
            try:
                instructor_department = instructor_info.find(
                    "div", {"class": "instructor-department caption-text color-black"}
                ).text
            except AttributeError:
                instructor_department = "None"
            if instructor_info.find("div", {"class": "instructor-expertise"}) != []:
                detail = instructor_info.find("div", {"class": "instructor-expertise"})
            else:
                detail = None

            if detail != None:
                learners = detail.find("span").text
                learners = int(re.sub("[^0-9.]+", "", learners))
                courses = detail.find("div", {"class": "courses-count"}).text
                courses = int(re.sub("[^0-9.]+", "", courses))
            else:
                learners = "None"
                courses = "None"

            instructor_information[instructor_name] = {
                "Instructor_title": instructor_title,
                "Instructor_department": instructor_department,
                "Learners": learners,
                "Open_courses": courses,
            }
    else:
        instructor_information = "None"
    return {
        "Enroll": enroll,
        "Views": views,
        "Instructor_info": instructor_information,
    }


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
        data[course] = crawl_add(link)

    if i % 10 == 0:
        print("Page {} out of {}...".format(i, page))
        # backup:

        with open(
            "backup/coursera_additional_backup{}.json".format(start),
            "w",
            encoding="utf-8",
        ) as json_file:
            json.dump(data, json_file)
        print("Saved backup")

# Save as json file
with open("output/additional_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file)
