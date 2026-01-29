#---------- Data Gathering---------

f = open("user_config.txt")
f=(f.readlines())

API_KEY           = f[0].split('\t:')[-1].strip()
USER_ID           = f[1].split('\t:')[-1].strip()
PASSWORD          = f[2].split('\t:')[-1].strip()
ROLES             = f[3].split('\t:')[-1].strip()
INPUT_RESUME_PATH = f[4].split('\t:')[-1].strip()
YEARS             = f[5].split('\t:')[-1].strip()
MONTHS            = f[6].split('\t:')[-1].strip()
LINKS             = f[7].split('\t:')[-1].strip()
TELEGRAM_TOKEN    = f[8].split('\t:')[-1].strip()
CHAT_ID           = f[9].split('\t:')[-1].strip()
#--------- Imports and setup-----------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--auto-open-devtools-for-tabs")

try:
    driver.quit()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=options)
except:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=options)
driver.maximize_window()
time.sleep(5)

#------------- Login ---------------

# Login

driver.get("https://www.linkedin.com/jobs/collections/easy-apply")
time.sleep(15)
U_NAME=driver.find_element(By.ID, "username")
U_NAME.clear()
U_NAME.send_keys(USER_ID)
U_PWD=driver.find_element(By.ID, "password")
U_PWD.clear()
U_PWD.send_keys(PASSWORD)
U_PWD.send_keys(Keys.ENTER)
time.sleep(15)

#search for the roles

search_box_input= driver.find_element(By.CLASS_NAME,"basic-input")
search_box_input.send_keys(ROLES)
search_box_input.send_keys(Keys.ENTER)
time.sleep(5)
for i in driver.find_elements(By.CLASS_NAME,"relative"):
    if i.text == "All filters":
        i.click()
time.sleep(5)
for i in driver.find_elements(By.CLASS_NAME,"search-reusables__secondary-filters-filter"):
    if " Easy Apply filter" in (i.text):
        toggle=driver.find_element(By.CLASS_NAME,"artdeco-toggle")
        toggle.click()
time.sleep(5)
button = driver.find_element(By.CSS_SELECTOR, '[data-test-reusables-filters-modal-show-results-button="true"]')
button.click()
time.sleep(7)

#----------------- functions -------------

def job_apply():
    try:
        button = driver.find_element(By.ID, "jobs-apply-button-id")
        button.click()
        xbutton = driver.find_element(By.ID, "jobs-apply-button-id")
        xbutton.click()
    except:
        try:
            button = driver.find_element(By.ID, "jobs-apply-button-id")
            button.click()
        except:
            send_message('error')
            

#--------------------------------------------------

def press_next():
    while(True):
        try:
            time.sleep(2)
            Next = driver.find_element(By.XPATH, "//*[@aria-label='Continue to next step']")
            Next.click()
            time.sleep(1)
            dismiss()
        except:
            try:
                Review = driver.find_element(By.XPATH, "//*[@aria-label='Review your application']")
                Review.click()
            except:
                try:
                    submit_application()
                except:
                    dismiss()
            break

#--------------------------------------------------
def submit_application():
    Submit = driver.find_element(By.XPATH, "//*[@aria-label='Submit application']")
    Submit.click()
#--------------------------------------------------

def dismiss():
    time.sleep(1)
    if len(driver.find_elements(By.CLASS_NAME,"artdeco-inline-feedback__icon")) != 0:
        button = driver.find_element(By.XPATH, "//*[@aria-label='Dismiss']")
        button.click()
        time.sleep(3)
        button = driver.find_element(By.XPATH, "//*[@data-control-name='save_application_btn']")
        button.click()
    else:
        press_next()

#--------------------------------------------------

def main():
        applied=[]
        x=driver.find_elements(By.CLASS_NAME,"job-card-list__entity-lockup")
        for i in x:
            print(i.text)
            driver.execute_script("arguments[0].scrollIntoView(true);",i)
            try:
                i.click()
            except:
                try:
                    dismiss()
                except:
                    continue
            time.sleep(5)
            try:
                if "Applied" in (driver.find_element(By.CLASS_NAME, "artdeco-inline-feedback__message").text):
                    applied.append(i.text)
                    continue
                else:
                    job_apply()
            except:
                try:
                    job_apply()
                except:
                    try:
                        send_message("error")
                        driver.refresh()
                        time.sleep(10)
                        dismiss()
                    except:
                        continue
            time.sleep(2)
            try:
                print('******* Applying********')
                press_next()
            except:
                try:
                    print('******* FAILED ********')
                    time.sleep(2)
                    dismiss()
                except:
                    continue
            time.sleep(7)
            try:
                print('*******Final Submit********')
                Final_submit=((driver.find_element(By.CLASS_NAME,"artdeco-modal__actionbar")).find_element(By.CLASS_NAME,"artdeco-button"))
                Final_submit.click()
                applied.append((i.text))
            except:
                continue
        jl=len(applied)
        return applied,jl
        

#-----------------------------------------------

if TELEGRAM_TOKEN and CHAT_ID is not None:
    import requests

    def send_message(message):
        token = TELEGRAM_TOKEN
        chat_id = CHAT_ID
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")
else:
    def send_message(message):
        print("You need Telegram Bot Configured")

#--------------------------------------------------

pg_no= driver.find_element(By.CLASS_NAME,"jobs-search-pagination__page-state")
max_pg=int(pg_no.text.split(" ")[-1])
tot=0
for i in range(max_pg):
    x=driver.find_elements(By.CLASS_NAME,"job-card-list__entity-lockup")
    for i in x:
        driver.execute_script("arguments[0].scrollIntoView(true);",driver.find_elements(By.CLASS_NAME,"job-card-list__entity-lockup")[-1])
        time.sleep(1)
    x=driver.find_elements(By.CLASS_NAME,"job-card-list__entity-lockup")
    print(len(x))
    time.sleep(2)
    print("start")
    try:
        job_list,no_applied=main()
    except:
        error_message = f"""!!! Execution Failed !!!"""
        send_message(error_message)
    message= f"""Number of Jobs Applied: {no_applied} \n\nThese are the list of jobs applied: \n\n"""
    for j in job_list:
        message=message+j+ '\n\n *************** \n\n'
    send_message(message)
    tot=tot+no_applied
    try:
        dismiss()
    except:
        print("something")
    time.sleep(4)
    print('next page')
    next_button = driver.find_element(By.XPATH, "//*[@aria-label='View next page']")
    next_button.click()
    time.sleep(5)


print("Stuff works")