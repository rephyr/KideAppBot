"""
Kide.App.Bot.By.ES VERSIO 1.2

This Python script automates the process of logging into the kide.app website and refreshing the page until a ticket is available for purchase. 
Once a ticket is available, the script will automatically add it to the shopping cart.

The script uses Selenium WebDriver for automating the web interactions.

Functions included in this script are:
- log_in: Logs into the kide.app website using provided email and password.
- add_to_cart: Adds a ticket to the shopping cart when it becomes available.
- check_time: Checks the current time in Helsinki.
- check_if_cart_exists: Checks if the ticket can be added to the shopping cart.
- find_id_of_selector: Finds the ID of the selector for the ticket quantity dropdown.
- max_ticket_count: Determines the maximum number of tickets that can be selected.
- select_ticket: Selects a specified number of tickets from the dropdown.

Usage:
- Update the 'codes' dictionary with your email and password.
- Update the 'path' variable with the location of your ChromeDriver.
- Update the 'driver.get' method with the URL of the event you want to purchase tickets for.
- Update the 'when_ticket_sales_start' variable with the time when the ticket sales start.
- Run the script before the ticket sales start. The script will handle the rest.
"""

import pytz
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

import time

# Dictionary with email address and password.
emailPassword = {
    "email": "" ,  # Enter email here
    "password": ""  # Enter password here
}

def log_in(email: str, password: str, driver: webdriver.Chrome) -> None:
    """
    Logs into kide.app when the "Log in" text is visible in the top right corner.
    
    Parameters:
    email (str): Email used for logging in.
    password (str): Password used for logging in.
    driver (webdriver.Chrome): WebDriver instance used when interacting with the web page.
    """

    # finds the "Log in" text and clicks it.
    
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "o-action-chip--primary-dark")))
    element.click()

    time.sleep(0.5)

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//o-menu-item[contains(text(), 'Kirjaudu sisään')]")))
    element.click()

    username_box = driver.find_element(By.ID, "username")
    username_box.send_keys(email)

    password_box = driver.find_element(By.ID, "password")
    password_box.send_keys(password)


    print("Log in: Succesful")
    print("Continuing soon")
    time.sleep(5)



def add_to_cart(driver: webdriver.Chrome) -> None:
    """
    Adds a ticket to the shopping cart when it becomes available.
    
    Parameters:
    driver (webdriver.Chrome): WebDriver instance used when interacting with the web page.
    """

    cart = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//o-item[@class="o-align-items--flex-start"]')))
    cart.click()

    indeksi = find_id_of_selector(driver)

    select = Select(
        driver.find_element(By.XPATH, f'//*[@id="input-{indeksi}"]'))

    max_ticket_count(select)

    tilaa = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Siirry tilaamaan')]")))
    tilaa.click()


def find_id_of_selector(driver):
    # Find the correct selector index for the ticket quantity dropdown

    index = 1
    while True:
        xpath = f'//*[@id="input-{index}"]'
        print(xpath)
        if check_if_cart_exists(driver, xpath) is False:
            index += 1
        else:
            return index


def check_time(numero):
    """
    Checks the current time in Helsinki.
    :return: The current time as a string.
    """

    timezone_helsinki = pytz.timezone("Europe/Helsinki")
    datetime_helsinki = datetime.now(timezone_helsinki)

    if numero == 0:
        aika = datetime_helsinki.strftime(f"%H:%M:%S")
    elif numero == 1:
        aika = datetime_helsinki.strftime(f"%H:%M:%S.%f")[:-3]

    return aika


def check_if_cart_exists(driver, xpath):
    """
    Checks if the ticket can be added to the shopping cart.
    :param driver: WebDriver instance.
    :param xpath: XPath of the cart element.
    :return: True if the cart element exists, False otherwise.
    """

    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def wait(saleStartTime):

    while True:

        if check_time(0) >= saleStartTime:
            print("Status: Clear")
            break

        else:
            aika = check_time(0)
            print("Status: Waiting")
            print(f"Current time: {aika}")
            print(f"Target time: {saleStartTime}")

            continue


def select_ticket(index, select):
    try:
        index = str(index)
        select.select_by_visible_text(index)
    except NoSuchElementException:
        return False
    return True

def max_ticket_count(select):

    options = 1
    while True:
        if select_ticket(options, select) is True:
            options += 1
        else:
            return None


def main():
    # Path to chromedriver on your computer
    path = ""
    driver = webdriver.Chrome(path)

    # URL of the kide.app event page
    driver.get("https://kide.app/fi/events/b98a17d0-7670-4b37-933b-cf122d4aa2de")
    ind = 0

    # Time (in HH:MM:SS) a minute before ticket sales start
    # For example, if sales start at 15:00:00, set this to 14:59:00

    ticketSaleStart = "09:59:00"



    try:


        cart_xpath = '//o-item[@class="o-align-items--flex-start"]'
        # Wait until the ticket sale start time

        wait(ticketSaleStart)

        while True:

            if check_if_cart_exists(driver, cart_xpath) is True:

                add_to_cart(driver)

                time_bought = check_time(1)

                print(f"Tickets added to cart. "
                      f"Current time is: {time_bought}" )

                time.sleep(5)
                break
            else:
                ind += 1
                print(f"Times refreshed: {ind}")

                driver.refresh()

                time_right_now = check_time(0)
                print(f"Time: {time_right_now}")

                time.sleep(0.6)  # Tähän kuinka nopee haluut päivittää sivua.
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
