# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    format='%(asctime)s %(message)s',
    level=logging.INFO,
    datefmt='%b %d %H:%M:%S')


# Start the browser and login with standard_user
def login (user, password):
    logging.info('Starting the browser...')
    options = ChromeOptions()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    logging.info('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    input_username = driver.find_element(By.ID, 'user-name')
    input_password = driver.find_element(By.ID, 'password')
    btn_login = driver.find_element(By.ID, 'login-button')

    input_username.send_keys(user)
    input_password.send_keys(password)
    btn_login.click()

    if driver.current_url == 'https://www.saucedemo.com/inventory.html':
        logging.info('Successfully logged in with user: ' + user)
        return driver
    else:
        logging.info('Failed to logged in')
        return False

def add_items_to_cart(driver, total_items):
    logging.info('add_items_to_cart')
    wait = WebDriverWait(driver, 0) 

    items = driver.find_elements(By.CLASS_NAME, 'inventory_item')[:total_items]

    for item in items:
        product_name = item.find_element(By.CLASS_NAME, 'inventory_item_name').text
        item.find_element(By.CSS_SELECTOR, "button.btn_inventory")
        add_to_cart_button = item.find_element(By.CSS_SELECTOR, 'button.btn_inventory') 
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn_inventory')))
        add_to_cart_button.click()

        logging.info ('add items to cart: ' + product_name)
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    total_items = int(cart_badge)
    logging.info('total_items_in_cart: %d', total_items)
    assert total_items == total_items, f'Expected to add {total_items} items, but added {total_items}.'
    return total_items == total_items

def remove_all_items(driver):
    wait = WebDriverWait(driver, 0) 
    
    cart_link = driver.find_element(By.CSS_SELECTOR, "a[class='shopping_cart_link']")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='shopping_cart_link']")))
    cart_link.click()
    
    items = driver.find_elements(By.CLASS_NAME, "cart_item")
    for item in items:
        product_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
        item.find_element(By.CLASS_NAME, "cart_button").click()
        logging.info ('remove items from cart: ' + product_name)
    
    items_after_removal = driver.find_elements(By.CLASS_NAME, "cart_item")
    all_items_removed = len(items_after_removal) == 0
    
    assert all_items_removed, "Not all items were removed from the cart"
    logging.info('All items removed from cart: %s', all_items_removed)
    
    return all_items_removed

if __name__ == "__main__":
    total_items = 5
    driver = login('standard_user', 'secret_sauce')
    add_items_to_cart(driver, total_items)
    remove_all_items(driver)
    driver.quit()