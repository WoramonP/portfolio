"""
This program adds transcription to the Thai phrases. For example:
    Original text: In Thai, Hello is สวัสดี.
    After the program: In Thai, Hello is สวัสดี (sa wat dee).

Transcription is from the website: http://www.thai-language.com/?nav=dictionary&anyxlit=1
Website to be opened with Google Chrome.

Author: Woramon P.
Date: 5/29/22
"""

import re
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# get the text and extract Thai phrases
with open("1_original_text.txt", encoding="utf-8") as fh:
    content = fh.read()

pattern = re.compile(r"([\u0E00-\u0E7F]+)")  # pattern to identify Thai phrases
# include () in the pattern, this will be important when we do re.split() later
# https://stackoverflow.com/questions/2136556/in-python-how-do-i-split-a-string-and-keep-the-separators
thai_phrases = "\n".join(set(re.findall(pattern, content)))

# get transcription from the website
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = 'http://www.thai-language.com/?nav=dictionary&anyxlit=1'
driver.get(url)

driver.find_element(by=By.NAME, value='anyx').send_keys(thai_phrases)
time.sleep(0.2)

driver.find_element(by=By.XPATH, value='//*[@id="submit1"]').click()
time.sleep(0.2)

xpath_result = '//*[@id="old-content"]/table[1]/tbody'
thai_transcription = driver.find_element(by=By.XPATH, value=xpath_result).text

# create a dict for each Thai phrase and its transcription
t_dict = {}
for string in thai_transcription.split("\n"):
    thai, transcription = string.split(" ", 1)
    transcription_without_tone = ' '.join(word[:-1] for word in transcription.split())
    # remove tone marks for easy reading
    t_dict[thai] = transcription_without_tone
    print(thai)
    print(transcription_without_tone)  # print this out for inspection

# add transcription after each Thai phrase
# I use re.split() and loop through each segment; if matched, then add transcription to the segment

# reason for not using str.replace()
# if a phrase has a sub-string (such as สวัสดีครับ has a sub-string สวัสดี), it may be replaced twice.

content_split = re.split(pattern, content)
for index, segment in enumerate(content_split):
    if segment in t_dict:
        content_split[index] += f" ({t_dict[segment]})"

with open("2_output_with_Thai_transcription.txt", "w", encoding="utf-8") as fh:
    fh.write("".join(content_split))

# finally, inspect the printed transcription for errors and fix them in the file
# this is because the website's transcription may not always be accurate
