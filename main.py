import time
import math
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

DRIVER_PATH = r"C:/Users/gabri/Mine/apps/chromedriver/chromedriver.exe"
BASE_URL = "https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Pistol&category_730_Type%5B%5D=tag_CSGO_Type_SMG&category_730_Type%5B%5D=tag_CSGO_Type_Rifle&category_730_Type%5B%5D=tag_CSGO_Type_SniperRifle&category_730_Type%5B%5D=tag_CSGO_Type_Shotgun&category_730_Type%5B%5D=tag_CSGO_Type_Machinegun&category_730_Type%5B%5D=tag_CSGO_Type_Knife&category_730_Type%5B%5D=tag_Type_Hands&category_730_Type%5B%5D=tag_CSGO_Tool_Patch&category_730_Type%5B%5D=tag_CSGO_Tool_WeaponCase_KeyTag&category_730_Type%5B%5D=tag_CSGO_Type_Ticket&appid=730#p"
FINAL_TAG = "_price_asc"
number = int()

options = Options()
options.headless = True
options.add_argument("--window.size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

def stepThroughPages(posts, pageNumber):
    driver.get(BASE_URL+str(pageNumber)+FINAL_TAG)
    time.sleep(15)
    soup = BeautifulSoup(driver.page_source, "html5lib")

    TotalResult = soup.find("span", id="searchResults_total").text
    TotalResult = TotalResult.split(".")
    TotalResults = TotalResult[0] + TotalResult[1]

    
    posts.extend(soup.find_all("div","market_listing_row market_recent_listing_row market_listing_searchresult"))

    if pageNumber >= 7 or pageNumber >= 770: return posts
    pageNumber += 1
    return stepThroughPages(posts, pageNumber)


totalPosts = stepThroughPages([], 1)
print(len(totalPosts))
for i, post in enumerate(totalPosts):
    postTitle = post.find("span","market_listing_item_name").get_text()
    postPrice = post.find("span","normal_price").get_text()
    postQuantity = post.find("span","market_listing_num_listings_qty").get_text()
    lali = postPrice.split("$")
    porn = lali[1:3]
    loki = "$", porn[0].split(" ")[0], "$",porn[1].split(" ")[0], "USD"
    loki = str(loki).split("'")
    LOKI = loki[1]+loki[3]+" "+loki[9]
    postIVA = round(float(loki[3])/1.15-0.01, 2)
    postIVA = postIVA
    lel = "| After tax: "
    print(f"{i+1}: {postTitle} {postQuantity} {str(LOKI)} {lel} {postIVA}")

driver.quit()