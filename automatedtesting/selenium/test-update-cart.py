# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import logging

logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.INFO,
    datefmt='%b %d %H:%M:%S')


# Start the browser and login with standard_user
def login (user, password):
    print ('Starting the browser...')
    options = ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    print ('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    input_username = driver.find_element(By.ID, 'user-name')
    input_password = driver.find_element(By.ID, 'password')
    btn_login = driver.find_element(By.ID, 'login-button')

    input_username.send_keys(user)
    input_password.send_keys(password)
    btn_login.click()

    if driver.current_url == 'https://www.saucedemo.com/inventory.html':
        logging.info('Successfully logged in with user: ' + user)
        return True
    else:
        logging.info('Failed to logged in')
        return False

def add_items_to_cart(driver, total_items):
    logging.info('add_items_to_cart')
    n_items = 0
    for i in range(total_items):
        try:
            cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
            n_items = int(cart_badge)
        except NoSuchElementException:
            logging.info("Cart is empty.")


        product_link = driver.find_element(By.ID, "item_" + str(i) + "_title_link")
        product_name = product_link.find_element(By.CLASS_NAME, "inventory_item_name").text
        product_link.click()

        n_items += 1
        time.sleep(2) 
        logging.info ('add_items_to_cart: ' + product_name)
        driver.find_element(By.ID, "back-to-products").click()
    return n_items > 0

def remove_all_items():
  driver.get("https://www.saucedemo.com/cart.html")
  items = driver.find_elements(By.CLASS_NAME, "cart_item")
  for item in items:
    item.find_element(By.CLASS_NAME, "cart_button").click()
  items = driver.find_elements(By.CLASS_NAME, "cart_item")
  print ('Remove all items completed!')
  return len(items) == 0

if __name__ == "__main__":
    total_items = 3
    driver = login('standard_user', 'secret_sauce')
    add_items_to_cart(driver, total_items)
    remove_all_items()
    driver.quit()