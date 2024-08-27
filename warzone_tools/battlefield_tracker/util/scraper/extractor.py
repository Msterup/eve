from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time, re, json, redis
if __name__ == "__main__": # for local debug
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from battlefield_tracker.util.scraper.redis_helper import update_advantage_in_redis

# for quick debug of depedent functions
def persist_to_file(file_name):

    def decorator(original_func):

        try:
            cache = json.load(open(file_name, 'r'))
        except (IOError, ValueError):
            cache = {}

        def new_func(param):
            if param not in cache:
                cache[param] = original_func(param)
                json.dump(cache, open(file_name, 'w'))
            return cache[param]

        return new_func

    return decorator

def fill2faction(fill):
    if fill == '#00ACD1':
        return "caldari"
    if fill == "#43AA60":
        return "gallente"
    if fill == "#FE3743":
        return "minmatar"
    if fill == "#E7B815":
        return "amarr"
    else:
        return "fill2faction was unable to map this faction color"

def get_faction(element):
    try:
        # Locate the SVG element within the given element (e.g., cols[0])
        svg_element = element.find_element(By.TAG_NAME, "svg") 
        path_element = svg_element.find_element(By.TAG_NAME, "path")

        # Get the 'fill' attribute from the SVG element
        fill_value = path_element.get_attribute("fill")
        return fill2faction(fill_value)
    except Exception as e:
        print("Error retrieving SVG fill:", e)
        return None
    
def assign_advantage(system_data, is_attack, advantage_type, value):
    defender = system_data["defender"]

    if defender == "amarr":
        attacker = "minmatar"
        if is_attack:
            player = "minmatar"
        else:
            player = "amarr"
    if defender == "minmatar":
        attacker = "amarr"
        if is_attack:
            player = "amarr"
        else:
            player = "minmatar"
    
    if defender == "caldari":
        attacker = "gallente"
        if is_attack:
            player = "gallente"
        else:
            player = "caldari"
    if defender == "gallente":
        attacker = "caldari"
        if is_attack:
            player = "caldari"
        else:
            player = "gallente"

    key = f"{player}_{advantage_type}"
    system_data[key] = int(value)
    system_data["attacker"] = attacker

#@persist_to_file('/warzone_tools/cache.dat') # For debug
def get_adv_data(faction, desired_status):
    gecko_driver_path = '/usr/local/bin/geckodriver'
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Run in headless mode
    firefox_options.add_argument('--window-size=800,400')  # Set the window size

    # Create and configure a Firefox profile
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("toolkit.cosmeticAnimations.enabled", False)  # Disable animations
    firefox_profile.set_preference("layout.css.scroll-behavior.enabled", False)  # Disable smooth scrolling
    firefox_profile.set_preference("general.smoothScroll", False)  # Disable smooth scrolling
    firefox_profile.set_preference("media.peerconnection.enabled", False)  # Disable WebRTC
    firefox_profile.set_preference("webgl.disabled", True)  # Disable WebGL

    # Merge the profile into the options
    firefox_options.profile = firefox_profile

    # Set up the Firefox service
    service = Service(gecko_driver_path)

    # Initialize the Firefox WebDriver with the service and options
    driver = webdriver.Firefox(service=service, options=firefox_options)

    url = f'https://www.eveonline.com/frontlines/{faction}'
    driver.get(url)
    retrival_time = datetime.now().isoformat()

    # Wait until the page is fully loaded
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )
    driver.execute_script("""
        window.requestAnimationFrame = function(callback) {
            setTimeout(function() { callback(Date.now()); }, 1000 / 2);  // Limit to 2 FPS
        };
    """)

    # Scroll to the element with the text "Warzone Map" and wait for it to load
    target_xpath = "//p[@class='message-headline' and text()='Warzone Map']"
    full_table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, target_xpath))
    )
    driver.execute_script("arguments[0].scrollIntoView();", full_table)
    driver.execute_script("window.scrollBy(0, -100);")  # Adjust the value as needed

    # Find and click table button
    table_button_xpath = "//span[text()='Details']"
    table_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, table_button_xpath))
    )
    table_button.click()
    
    # Locate the specific table by its class
    table_xpath = "//table[contains(@class, 'mantine-Table-root mantine-WarzoneTable-root mantine-WarzoneTable-selectedText')]"

    # Find all rows within this table
    # TODO: scan with interval should depend on system status, eg, scan frontlines often


    table_rows = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, f"{table_xpath}//tbody/tr"))
    )
    scrollable_container = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'mantine-ScrollArea-viewport')]"))
    )
    # Locate the "Allow all" button using its text
    allow_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Allow all')]"))
    )
    # Click the button to dismiss the cookie banner
    allow_all_button.click()


    redis_client = redis.StrictRedis(host='redis', port=6379, db=1)
    regex = re.compile(r'(\d+)%')
    data = {"timestamp": retrival_time,
            "faction": faction}
    for idx, row in enumerate(table_rows):
        system_data = {}
        # Scroll the row into view
        if idx == 0:
            time.sleep(4)
        cols = row.find_elements(By.TAG_NAME, "td")
        # Get data from cols
        status = cols[3].text
        if status != desired_status:
            continue # TODO: make better solution

        system_data["status"] = status
        system_data["system"] = cols[1].text 
        system_data["defender"] = get_faction(cols[0])
        system_data["contested"] = cols[4].text.strip('%')
        system_data["base_advantage"] = cols[5].text.strip('%')
        system_data["update_advantage"] = False

        swing = update_advantage_in_redis(redis_client, system_data["system"], "base_advantage", system_data)
        if swing != 0:
            system_data["update_advantage"] = True
        
            driver.execute_script("arguments[0].scrollIntoView();", scrollable_container, cols[0])
            driver.execute_script("arguments[0].scrollIntoView();", full_table)
            driver.execute_script("window.scrollBy(0, -100);")  # Adjust the value as needed
            driver.execute_script("arguments[0].click();", cols[0])
            
            time.sleep(1)  # Optional: wait for the scrolling to complete
            looplist = [(True, "attacker"), (False, "defender")]
            for is_attack, player in looplist:
                hover_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, '{player}Advantage')]"))
                )
                actions = ActionChains(driver)
                actions.move_to_element(hover_element).perform()
                time.sleep(6)
                objectives_div = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Completed Objectives:')]"))
                )
                systems_div = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Neighboring Systems:')]"))
                )
                match = regex.search(objectives_div.text)
                assign_advantage(system_data, is_attack, "objectives_advantage", match.group(1))
                match = regex.search(systems_div.text)
                assign_advantage(system_data, is_attack, "systems_advantage", match.group(1))
        print(f"Gathered data: {system_data}")
        data[system_data["system"]] = system_data

    driver.quit()
    return data




if __name__ == "__main__":#
    #data = get_basic_data()
    #adv_data = get_adv_data("caldari", "Command Operations")
    adv_data = get_adv_data("caldari", "Frontline")