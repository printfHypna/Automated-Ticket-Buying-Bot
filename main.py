from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import WebDriverException
from time import sleep
from datetime import datetime


def wait(by, text, time=5):
    WebDriverWait(driver, time).until(
    EC.presence_of_element_located((by, text))
)
    
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def wait_error(xpath, time=5):
    try:
        wait(By.XPATH, xpath, time)
    except TimeoutException:
        return False
    return True

base_url = ('https://www.passo.com.tr/tr')

service = Service(executable_path=
                  "/Users/kutayozdur/Documents/PythonProjects/PassoLigTicket/chromedriver")
driver = webdriver.Chrome(service=service)

driver.get(base_url)

driver.maximize_window()

# CLOSING COOKIE BANNER
if wait_error("//div[@class='cc-compliance']"):
    cookie_banner = driver.find_element(By.XPATH, "//div[@class='cc-compliance']")
    cookie_banner.click()
else:
    pass

# CLOSING AD IF EXISTS 
while True:

    if wait_error("//*[contains(text(), 'KAPAT')]"):
        close_ad = driver.find_element(By.XPATH, "//*[contains(text(), 'KAPAT')]")
        try:
            close_ad.click()
            break
        except ElementClickInterceptedException:
            continue
    else:
        break

# Open login page

wait(By.PARTIAL_LINK_TEXT, "GİRİŞ YAP")
link = driver.find_element(By.PARTIAL_LINK_TEXT, "GİRİŞ YAP")
link.click()

# Login 

wait(By.CLASS_NAME, "quick-input")
login_inputs = driver.find_elements(By.CLASS_NAME, "quick-input")

login_inputs[0].clear()
login_inputs[0].send_keys("kutayozdur@gmail.com")

login_inputs[1].clear()
login_inputs[1].send_keys("Kutayke54")

# Check if we are back in main page after the login
while(driver.current_url != base_url):
    sleep(2)

# Event search

event = "trabzonspor"

wait(By.ID, "search_input")
event_input = driver.find_element(By.ID, "search_input")
event_input.clear()
event_input.send_keys(event + Keys.ENTER)

# Selecting event

game_index = 0
# If the game is at the bottom, scroll down
# if game_index > 1:
#     for handle in driver.window_handles:
#         driver.switch_to.window(handle)
#         driver.execute_script("window.scrollTo(0, 200);")

wait(By.CLASS_NAME, "col-md-4")
while True:
    try:
        if game_index > 1:
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                driver.execute_script("window.scrollTo(0, 200);")
        game_links = driver.find_elements(By.CLASS_NAME, "col-md-4")
        game_links[game_index].click()
        break
    except IndexError:
        print("Game isn't avaliable yet!")
        driver.refresh()
        sleep(1)

# Clicking buy button
# Closing privileged card window if it pops up
        
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    driver.execute_script("window.scrollTo(0, 700);")

privileged_card_window_xpath = "//button[@class='btn btn-secondary btn-lg']"
wait(By.XPATH, "//button[@class='red-btn']")
red_button = driver.find_element(By.XPATH, "//button[@class='red-btn']")

now = datetime.now()
start_time = now
print(start_time)
current_url = driver.current_url
while not current_url.__contains__('koltuk-secim'):
    current_url = driver.current_url
    now = datetime.now()
    current_time = now
    print(current_time)
    running_time = current_time - start_time
    seconds = running_time.seconds
    if seconds > 30:
        driver.refresh()
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            driver.execute_script("window.scrollTo(0, 700);")
        start_time = now
        wait(By.XPATH, "//button[@class='red-btn']", 0.5)
        red_button = driver.find_element(By.XPATH, "//button[@class='red-btn']")
    try:
        red_button.click()
        print("CLICKED THE RED BUTTON!!!")
        sleep(0.5)
    except ElementClickInterceptedException:
        print("RED BUTTON NOT AVALIABLE!")
        try:
            wait(By.XPATH, privileged_card_window_xpath, 0.5)
            priv_window = driver.find_element(By.XPATH, privileged_card_window_xpath)
            priv_window.click()
            print("CLOSE BUTTON CLICKED!!!")
        except ElementClickInterceptedException:
            print("CLICK INTERCEPTED")
            continue
        except ElementNotInteractableException:
            print("ELEMENT NOT INTERACTABLE")
            continue
    except StaleElementReferenceException:
        continue
    except TimeoutException:
        continue

# Category Selection
catogery_index = 8

wait(By.XPATH,
    "(//select[@class='form-control ng-untouched ng-pristine ng-valid'])[2]")
select_catogery = Select(driver.find_element(By.XPATH,
    "(//select[@class='form-control ng-untouched ng-pristine ng-valid'])[2]"))

while True:
    select_catogery.select_by_index(catogery_index)
    if wait_error("//button[@class='swal2-confirm swal2-styled']", 1):
        try:
            no_seat_button = driver.find_element(By.XPATH, "//button[@class='swal2-confirm swal2-styled']")
            no_seat_button.click()
            print("No avaliable seat for the catogery!")
            print(datetime.now())
            select_catogery.select_by_index(0)
            sleep(0.2)
        except StaleElementReferenceException:
            print(111)
            continue
        except NoSuchElementException:
            print(222)
            continue
        except WebDriverException:
            print(333)
            continue
    else:
        break

        
# Selecting number of tickets

ticket_amount_index = 1

# sleep(1)  # Using this because "wait" isn't enough for some reason 
wait(By.XPATH,
    "(//select[@class='form-control'])")
select_amount = Select(driver.find_element(By.XPATH,
    "(//select[@class='form-control'])"))
select_amount.select_by_index(ticket_amount_index)


# Selecting Block 

wait(By.ID, "blocks")
select_block = Select(driver.find_element(By.ID, "blocks"))
blocks_list = select_block.options
block_index = len(blocks_list)-1

while driver.current_url != "https://www.passo.com.tr/tr/sepet":
    
    try:
        select_block.select_by_index(block_index)
        block_index -= 1
        if block_index == 0:
            block_index = len(blocks_list)-1
        wait(By.ID, "best_available_button")
        final_button = driver.find_element(By.ID, "best_available_button")
        final_button.click()
        if wait_error("(//button[@class='swal2-confirm swal2-styled'])"):
            close_button = driver.find_element(By.XPATH,
                "(//button[@class='swal2-confirm swal2-styled'])")
            close_button.click()
        else:
            continue
    except StaleElementReferenceException:
        continue
        
driver.quit()
