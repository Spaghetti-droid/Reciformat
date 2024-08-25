from reader.reader import Reader

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import validators

class SeleniumReader(Reader):
    """Gets the document from a URL Using a web browser
        Currently we only allow chrome, but selenium can use a number of other browsers
    """
    def handles(self, location: str) -> bool:
        if validators.url(location):
            return True
        return False
        
    
    def read(self, location: str) -> list:
        print(f'Making a request to {location}')
        chromeOptions = Options()
        chromeOptions.add_argument("--headless=new")
        driver = None
        try:
            driver = webdriver.Chrome(options=chromeOptions)
            driver.get(location)
            scripts = driver.find_elements(By.XPATH, "//script[@type='application/ld+json']")
            jsons = []
            for script in scripts:
                jsons.append(script.get_attribute('innerHTML'))
                
            return jsons
        finally:
            if driver:
                driver.quit()