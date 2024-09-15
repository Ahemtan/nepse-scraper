import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('window-size=600x400')
options.add_argument("disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

BASE_URL = "https://www.sharesansar.com/"

class NepseData:
    def __init__(self, scripts: str):
        self.scripts = scripts
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    def find_element_safe(self, xpath, retries=3, delay=2):
        for _ in range(retries):
            try:
                return self.driver.find_element('xpath', xpath)
            except NoSuchElementException:
                time.sleep(delay)
        raise NoSuchElementException(f"Element not found with xpath: {xpath}")

    def price_history(self):
        self.driver.get(BASE_URL)
        time.sleep(2)

        try:
            search_box = self.find_element_safe("//input[@placeholder = 'Company Name or Symbol']")
            search_box.send_keys(self.scripts)
            time.sleep(2)

            self.find_element_safe("//b[text() ='" + self.scripts.upper() + "']").click()
            time.sleep(2)

            self.find_element_safe("//a[text() = 'Price History']").click()
            time.sleep(2)

            self.find_element_safe("//option[text() = '50']").click()
            time.sleep(2)

            final_df = pd.DataFrame()
            while True:
                webpage = self.driver.page_source
                soup = BeautifulSoup(webpage, 'html.parser')

                table = soup.find('table', class_='table table-hover table-striped table-bordered compact dataTable no-footer')
                if not table:
                    print("Price history table not found.")
                    break

                rows = table.find_all('tr', role="row")
                extracted_data = []

                for row in rows[1:]: 
                    try:
                        cols = row.find_all('td')
                        if len(cols) == 9: 
                            RowDict = {
                                "Date": cols[1].text.strip(),
                                "Open": cols[2].text.strip().replace(',', ''),
                                "High": cols[3].text.strip().replace(',', ''),
                                "Low": cols[4].text.strip().replace(',', ''),
                                "Close": cols[5].text.strip().replace(',', ''),
                                "% change": cols[6].text.strip(),
                                "Volume": cols[7].text.strip().replace(',', ''),
                                "TurnOver": cols[8].text.strip().replace(',', '')
                            }
                            extracted_data.append(RowDict)
                    except Exception as e:
                        print(f"Error processing row: {e}")

                extracted_df = pd.DataFrame(extracted_data)
                final_df = pd.concat([final_df, extracted_df], ignore_index=True)

                try:
                    next_button = self.driver.find_element('xpath', "//a[text() = 'Next']")
                    if "disabled" in next_button.get_attribute("class"):
                        break
                    next_button.click()
                    time.sleep(2)
                except NoSuchElementException:
                    print("No 'Next' button found, ending pagination.")
                    break

            return final_df

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error encountered during scraping: {e}")
        finally:
            self.driver.quit()

price_history = NepseData("hrl")
data_df = price_history.price_history()

file_name = "hrl.csv"
data_df.to_csv("data/" + file_name, encoding='utf-8', index=False)
