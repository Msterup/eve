from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_web_data(target='Caldari'):
    gecko_driver_path = '/usr/local/bin/geckodriver'
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    service = Service(gecko_driver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)
    data = []

    try:
        # Open the webpage
        url = 'https://www.eveonline.com/frontlines/caldari'
        driver.get(url)

        # Confirm the driver is loading by checking the title
        WebDriverWait(driver, 10).until(
            EC.title_contains('Caldari | Frontlines | EVE Online')
        )
        print(f"Page title: {driver.title}")

        current_url = driver.current_url

        if 'eveonline.com/frontlines/caldari' not in current_url:
            print("Error: Not on the expected page.")
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

        try:
            # Wait for the element to be clickable
            element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/main/div/div/section[2]/div/div/div[2]/div/div/div/div/div[1]/div/div[1]/button[2]/span'))
            )
            element.click()
            print("Clicked the element with specified XPath.")
        except Exception as e:
            print(f"Error clicking element by XPath: {e}")

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'lxml')

        tbodies = soup.find_all('tbody')
        print(f"Number of <tbody> elements found: {len(tbodies)}")
        for tbody in tbodies:
            rows = tbody.find_all('tr')
            for row_index, row in enumerate(rows):
                cells = row.find_all('td')
                cell_data = [cell.get_text(strip=True) for cell in cells]
                
                #Get current owner
                path = cells[0].find('path')
                fill = path.get('fill')

                if fill == '#00ACD1':
                    owner = "Caldari"
                if fill == "#43AA60":
                    owner = "Gallente"
                if fill == "#FE3743":
                    owner = "Minmatar"
                if fill == "#E7B815":
                    owner = "Amarr"

                cell_data[0] = owner
                data.append(cell_data)
    finally:
        # Clean up and close the browser
        driver.quit()
        return data

if __name__ == "__main__":
    data = get_web_data()