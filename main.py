from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import html5lib
import time
import math



# Change BASE_URL to your liking
BASE_URL = "https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_Pistol&category_730_Type%5B%5D=tag_CSGO_Type_SMG&category_730_Type%5B%5D=tag_CSGO_Type_Rifle&category_730_Type%5B%5D=tag_CSGO_Type_SniperRifle&category_730_Type%5B%5D=tag_CSGO_Type_Shotgun&category_730_Type%5B%5D=tag_CSGO_Type_Machinegun&category_730_Type%5B%5D=tag_CSGO_Type_Knife&category_730_Type%5B%5D=tag_Type_Hands&category_730_Type%5B%5D=tag_CSGO_Tool_Patch&category_730_Type%5B%5D=tag_CSGO_Tool_WeaponCase_KeyTag&category_730_Type%5B%5D=tag_CSGO_Type_Ticket&appid=730#p"
FINAL_TAG = "_price_asc"
number = int()

options = Options()
options.headless = True
# window size argument is necessary because of the simulated window size
options.add_argument("--window.size=1920,1200")

# Initialize webdriver with selected options
driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())

# In charge of getting the page cache
def stepThroughPages(posts, pageNumber):
    driver.get(BASE_URL+str(pageNumber)+FINAL_TAG)
    time.sleep(15)
    soup = BeautifulSoup(driver.page_source, "html5lib")

    TotalResult = soup.find("span", id="searchResults_total").text
    TotalResult = TotalResult.split(".")
    TotalResults = TotalResult[0] + TotalResult[1]

    # Number of pages to search through
    Selected_Pagenumb = 75

    # In case you want the total amount of pages delete the previous definition
    #Selected_Pagenumb = Total Results
    
    posts.extend(soup.find_all("div","market_listing_row market_recent_listing_row market_listing_searchresult"))

    if pageNumber >= Selected_Pagenumb or pageNumber >= int(TotalResults): return posts
    pageNumber += 1
    return stepThroughPages(posts, pageNumber)


totalPosts = stepThroughPages([], 1)
# Reality check
print(len(totalPosts))

# In charge of getting every stat from each post
for i, post in enumerate(totalPosts):
    postTitle = post.find("span","market_listing_item_name").get_text()
    postPrice = post.find("span","normal_price").get_text()
    postQuantity = post.find("span","market_listing_num_listings_qty").get_text()
    Splitting = postPrice.split("$")
    Price = Splitting[1:3]
    Priceformat = "$", Price[0].split(" ")[0], "$",Price[1].split(" ")[0], "USD"
    Priceformat = str(Priceformat).split("'")
    Full_phrase = Priceformat[1]+Priceformat[3]+" "+Priceformat[9]
    postIVA = round(float(Priceformat[3])/1.15-0.01, 2)
    postIVA = postIVA
    print(f"{i+1}: {postTitle} {postQuantity} {str(Full_phrase)} | After tax: {postIVA}")

driver.quit()
