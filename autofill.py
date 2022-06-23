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

def fillText(driver, df, element_class, user_id):
    email = df["email"][user_id]
    name = df["name"][user_id]
    id_number = df["id"][user_id]
    phone = df["phone"][user_id]
    ig = df["instagram"][user_id]
    text_answers = [email, name, str(id_number), str(phone), ig]
    text_questions = driver.find_elements(By.CLASS_NAME, element_class)
    for a,q in zip(text_answers, text_questions):
        q.send_keys(a)
    return driver

def answerMCQ(driver, df, element_class, user_id):
    n = len(driver.find_elements(By.CLASS_NAME, element_class))
    i = random.randint(0, n-1)
    span_class = "aDTYNe.snByac.OvPDhc"
    size = driver.find_elements(By.CLASS_NAME, span_class)[i].text
    driver.find_elements(By.CLASS_NAME, element_class)[i].click()
    return driver, size

def fillAddress(driver, df, element_class, user_id):
    address = df["address"][user_id]
    text_answers = [address]
    text_questions = driver.find_elements(By.CLASS_NAME, element_class)
    for a,q in zip(text_answers, text_questions):
        q.send_keys(a)
    return driver

def submit(driver, element_class):
    driver.find_element(By.XPATH, element_class).click()
    return driver

def entryLog(url, df, size, user_id):
    email = df["email"][user_id]
    webhook = DiscordWebhook(url=os.getenv('WEBHOOK_URL'))
    spoiler_email = "||{}||".format(email)
    embed = DiscordEmbed(title="VinnieAIO Successful Entry", url=url, color=0x21333d)
    embed.add_embed_field(name="**Product**", value="Product Name", inline=False)
    embed.add_embed_field(name="**Size**", value=size, inline=False)
    embed.add_embed_field(name="**Store**", value="Store Name", inline=False)
    embed.add_embed_field(name="**Mode**", value="Raffle", inline=False)
    embed.add_embed_field(name="**Account**", value=spoiler_email, inline=False)
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    footer = 'VinnieAIO • Today at {}'.format(current_time)
    embed.set_footer(text=footer)
    webhook.add_embed(embed)
    webhook.execute()

df = pd.read_csv('googleForm.csv', dtype={'phone': str})

text_question_element_class = "whsOnd.zHQkBf"
mcq_element_class = "AB7Lab.Id5V1"
long_answer_element_class = "KHxj8b.tL9Q4c"
submit_element_class = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span'

url = "https://forms.gle/fx3iyi7EoEP6pnmv5"
s = Service("chromedriver")
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=s, options=chrome_options)
load_dotenv()
for user_id in range(len(df)):
    driver.get(url)
    driver = fillText(driver, df, text_question_element_class, user_id)
    driver, size = answerMCQ(driver, df, mcq_element_class, user_id)
    driver = fillAddress(driver, df, long_answer_element_class, user_id)
    driver = submit(driver, submit_element_class)
    entryLog(url, df, size, user_id)
driver.quit()