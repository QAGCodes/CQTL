from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

welcome_message = "\n\n\n\nHi! This is the CQTL (Co-Rec Queue Too Long) program.\n" \
                  "My purpose is to get information about occupancy rates\n" \
                  "from different locations in the Co-Rec and store them for later data\n" \
                  "processing! In other words, I will be able to tell you when is the perfect\n" \
                  "time to go to the gym so that you don't have to wait in line for long ;)\n\n" \
                  "Please leave this terminal open for me so I can work well :)\n" \
                  "Beginning data collection process...\n"


def get_gym_occupancy():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("chromedriver_win32/chromedriver.exe", options=chrome_options)

    url = "https://www.purdue.edu/recwell/facility-usage/index.php"
    driver.get(url)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, features="lxml")
    gym_locations = soup.find_all("div", class_="rw-c2c-feed__location")
    if len(gym_locations) == 0:
        return 0

    for index, location in enumerate(gym_locations):
        location_name = location.h5.text
        location_occupancy_div = location.find("div", class_="rw-c2c-feed__location--about")
        if location_occupancy_div.span.text == "Closed Now":
            continue
        location_occupancy = location_occupancy_div.find("span", class_="rw-c2c-feed__about--capacity").text
        location_time = location_occupancy_div.find("span", class_="rw-c2c-feed__about--update").text

        if "/" in location_name:
            location_name = location_name.replace("/", " ")
            location_name = location_name.replace("-", " ")
        with open(f'GymLog/{location_name}.txt', "a") as f:
            f.write(f'Name:{location_name} \n')
            f.write(f'{location_occupancy} \n')
            f.write(f'{location_time} \n\n')
    driver.quit()


if __name__ == "__main__":
    print(welcome_message)
    while True:
        status = get_gym_occupancy()
        if status == 0:
            print("Can't get gym information right now. Trying again...")
            continue
        else:
            print("Succeeded in grabbing info! Writing...")
        time_wait = 50  # 50 minutes wait
        print(f'waiting...')
        time.sleep(time_wait * 60)
