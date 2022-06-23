from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import random
import os

def fillText(driver, df, name, element_class, user_id):
    answer = df[name][user_id]
    text_answers = [str(answer)]
    text_questions = driver.find_elements(By.CLASS_NAME, element_class)
    for a,q in zip(text_answers, text_questions):
        q.send_keys(a)
    return driver

def answerMCQ(driver, element_class):
    n = len(driver.find_elements(By.CSS_SELECTOR, element_class))
    i = random.randint(0, n-1)
    span_class = "text-format-content"
    size = driver.find_elements(By.CLASS_NAME, span_class)[i].text
    driver.find_elements(By.CSS_SELECTOR, element_class)[i].click()
    return driver, size

def submit(driver, name, element_class):
    if name == 'email':
        driver.find_elements(By.CSS_SELECTOR, element_class)[1].click()
    else:
        driver.find_elements(By.CSS_SELECTOR, element_class)[2].click()
    return driver

def entryLog(url, df, size, user_id):
    email = df["email"][user_id]
    webhook = DiscordWebhook(url=os.getenv('WEBHOOK_URL'))
    spoiler_email = "||{}||".format(email)
    embed = DiscordEmbed(title="VinnieAIO Successful Entry", url=url, color=0x21333d)
    embed.add_embed_field(name="**Product**", value="Product Name", inline=False)
    embed.add_embed_field(name="**Size**", value=size, inline=False)
    embed.add_embed_field(name="**Store**", value="OurDailyDose Indonesia", inline=False)
    embed.add_embed_field(name="**Mode**", value="Raffle", inline=False)
    embed.add_embed_field(name="**Account**", value=spoiler_email, inline=False)
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    footer = 'VinnieAIO • Today at {}'.format(current_time)
    embed.set_footer(text=footer)
    webhook.add_embed(embed)
    webhook.execute()

df = pd.read_csv('googleForm.csv', dtype={'phone': str})

text_question_element_class = "office-form-question-textbox.office-form-textfield-input.form-control.office-form-theme-focus-border.border-no-radius"
mcq_element_class = "input[type='radio']"
submit_element_class = '.button-content'

s = Service("chromedriver")
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=s, options=chrome_options)
load_dotenv()

def loop_entry(driver):
    for user_id in range(len(df)):
        driver.get(url)
        driver.implicitly_wait(2)
        driver = fillText(driver, df, "email", text_question_element_class, user_id)
        driver = submit(driver, "email", submit_element_class)
        driver.implicitly_wait(2)
        driver = fillText(driver, df, "name", text_question_element_class, user_id)
        driver = submit(driver, "name", submit_element_class)
        driver.implicitly_wait(2)
        driver = fillText(driver, df, "id", text_question_element_class, user_id)
        driver = submit(driver, "id", submit_element_class)
        driver.implicitly_wait(2)
        driver = fillText(driver, df, "phone", text_question_element_class, user_id)
        driver = submit(driver, "phone", submit_element_class)
        driver.implicitly_wait(2)
        driver = fillText(driver, df, "instagram", text_question_element_class, user_id)
        driver = submit(driver, "instagram", submit_element_class)
        driver.implicitly_wait(2)
        driver, size = answerMCQ(driver, mcq_element_class)
        driver = submit(driver, "size", submit_element_class)
        driver.implicitly_wait(2)
        driver = fillText(driver, df, "address", text_question_element_class, user_id)
        driver = submit(driver, "address", submit_element_class)
        entryLog(url, df, size, user_id)

try:
    url = input("Enter the url: ")
    loop_entry(driver)
except Exception as e:
    print("Invalid input! Please try again.\n")
    url = input("Enter the url: ")
    loop_entry(driver)
    
driver.quit()