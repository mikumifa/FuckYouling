from time import sleep

import requests
import json
import csv

import retry
from retrying import retry

from sign import getSign
from sign505 import getSign505


@retry(wait_fixed=2000, stop_max_attempt_number=3)
def make_request(url, header, date):
    res = requests.post(url, headers=header, json=date)
    res.raise_for_status()
    return res


course_list_payload = {
    "albumGoodsId": "108745",
    "choice": False,
    "currentPage": 0,
    "pageSize": 30,
    "sortType": "asc"
}
timestamp = "1699171687"
useId = "6007476"
sign = getSign(timestamp)
sign505 = getSign505(course_list_payload, timestamp, useId)

csv_file_name = "course_data.csv"
course_headers = {
    'Host': 'new-app-api.ylyk.com',
    'Accno': '',
    'Token': 'b746c472b4fb6be80aa0e0bd232b325c',
    'Userid': '6007476',
    'Downloadchannel': 'home',
    'Channel': 'Android',
    'Accountid': 'ylyk_app',
    'Systeminfo': '9;M973Q',
    'Timestamp': timestamp,
    'Sign': sign,
    'Sign505': sign505,
    'Version': '5.7.1',
    'Buildversion': '23102601',
    'Anonymousid': 'cf514ff1a936d6f7',
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': '87',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.9.0'
}
course_list_url = "https://new-app-api.ylyk.com/v1/goods/getFilterAlbumCourseGoodsList"

response = make_request(course_list_url, course_headers, course_list_payload)
course_data = response.json()
data_list = []
print("Fetching course list...")
for course in course_data["data"]["list"]:
    course_id = course["courseId"]
    course_name = course["courseGoodsName"]
    question_url = "https://new-app-api.ylyk.com/v1/goods/course/getQuestions"
    question_payload = {
        "courseId": course_id
    }
    question_headers = {
        'Host': 'new-app-api.ylyk.com',
        'Content-Length': '20',
        'Deviceid': 'cf514ff1a936d6f7',
        'Version': '5.7.1',
        'Sign': sign,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; M973Q Build/PQ3A.190605.10261546; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.114 Mobile Safari/537.36',
        'Anonymousid': 'cf514ff1a936d6f7',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Timestamp': timestamp,
        'Userid': '6007476',
        'Buildversion': '23102601',
        'Channel': 'Android',
        'Token': 'b746c472b4fb6be80aa0e0bd232b325c',
        'Sign505': 'aba86d4ca744814e7611710cd68eb2b4',
        'Accountid': 'ylyk_app',
        'Origin': 'https://new-wx.ylyk.com',
        'X-Requested-With': 'com.zhuomogroup.ylyk',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://new-wx.ylyk.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = make_request(question_url, question_headers, question_payload)
    question_data = response.json()

    question_items = question_data["data"]["questionItems"]
    for index, item in enumerate(question_items):
        question_stem = item["questionStem"]
        question_type = item["questionType"]
        question_choices = item["questionAnswer"]
        data_list.append([course_id, index + 1, course_name, question_stem, question_type, question_choices])
    print(f"Processed course ID: {course_id}")
    sleep(10)
correct_answers = []

for item in data_list:
    question_choices = item[5]
    correct_answer = [choice["answerKey"] for choice in question_choices if choice["isRight"] == 1][0]
    correct_answer_value = [choice["answerValue"] for choice in question_choices if choice["isRight"] == 1][0]
    correct_answers.append((item[0], item[1], item[2], item[3], item[4], correct_answer, correct_answer_value))

with open(csv_file_name, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        ["Course ID", "No", "Course Name", "Question Stem", "Question Type", "Answer Key", "Answer Value"])
    csv_writer.writerows(correct_answers)

print(f"Data saved to {csv_file_name}")
