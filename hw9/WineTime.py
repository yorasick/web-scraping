from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WineTimeParser:
    url = "https://www.winetime.com.ua"

    driver = None

    
    def __init__(self):
        self.driver = webdriver.Chrome()


    def __del__(self):
        self.driver.quit()


    def parse_whisky_list(self, max_page: int):
        page = 1
        while page <= max_page:
            products = self.parse_page(page)
            if len(products) == 0:
                break
            yield products
            page += 1


    def parse_page(self, page: int):
        self.driver.get(f"{self.url}/ua/viski?page={page}")

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "products-column")))

        products = []

        products_column = self.driver.find_element(By.CLASS_NAME, "products-column")
        products_list = products_column.find_elements(By.CLASS_NAME, "product-micro")
    
        for product in products_list:
            id = int(product.find_element(By.CSS_SELECTOR, "[data-productkey]").get_attribute("data-productkey"))
            # TODO: HELP: why .text is not working here?
            name = product.find_element(By.CLASS_NAME, "product-micro--title").get_attribute('innerHTML')
            url = product.get_attribute("href")

            fav_button = product.find_element(By.CLASS_NAME, "the-fav-button")
            row = fav_button.find_element(By.XPATH, "../..")
            
            # Get the first div containing price info
            price_container = row.find_element(By.TAG_NAME, "div")

            # Get the price text element
            try:
                price_text = price_container.find_element(By.TAG_NAME, "div").get_attribute('innerHTML')
                price = int(price_text.strip().split('<span')[0])
            except:
                price = 0

            # Try to find old price element, default to 0 if not found
            try:
                price_text = price_container.find_element(By.CLASS_NAME, "c-grey").get_attribute('innerHTML')
                old_price = int(price_text.strip().split('<span')[0])
            except:
                old_price = 0

            products.append({
                "id": id,
                "title": name,
                "url": url,
                "prices": {
                    "price": price,
                    "old_price": old_price
                }
            })
            
        return products
