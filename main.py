import json
import time
from splinter import Browser
from datetime import datetime as dt

from EmailParser import EmailParser 
from Bill import Bill

BANK_INFO = '.bank_info.json'
MONTHLY_BILL_INFO = '.bill_info.json'

def get_transaction_info(search_value,
        search_field_xpath = '//*[@id="filteringText"]',
        match_table_xpath = '/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/div/div[1]/div/div/div[2]/div[2]/div[3]/table'):

    browser.find_by_xpath(search_field_xpath).fill(search_value)
    element = browser.find_by_xpath(match_table_xpath).first
    transaction_list = element.value.splitlines()

    date = dt.strptime(transaction_list[1].replace('/','-'), '%m-%d-%Y')
    description = transaction_list[2]
    amount = float( transaction_list[3][2:] )

    return date, description, amount

with open(".last_run_date.txt") as date_file:
    last_run_date = dt.strptime(date_file.readline().strip(), "%Y-%m-%d %H:%M:%S")

with open('.textbelt_api_key.txt') as key:
    api_key = key.readline().strip()

with open(BANK_INFO) as bank_file:
    bank_login_info = json.load(bank_file)

with open(MONTHLY_BILL_INFO) as bill_file:
    monthly_charge_data = json.load(bill_file)

with Browser(headless=True) as browser:
    # Visit URL
    url = "https://www.elevationscu.com"
    browser.visit(url)

    login_btn_xpath = '/html/body/div[1]/div[1]/header/div/div/div/div/div[2]/ul/li[2]/a'
    login_btn = browser.find_by_xpath(login_btn_xpath)
    login_btn.click()

    # login
    usr_name_xpath = '//*[@id="field-personal-userid-input"]'
    browser.find_by_xpath(usr_name_xpath).fill(bank_login_info['username'])
    usr_name_xpath = '//*[@id="field-personal-password-input"]'
    browser.find_by_xpath(usr_name_xpath).fill(bank_login_info['password'])
    login_btn_xpath = "/html/body/div[1]/div[1]/main/div/div/div/div/div[2]/div[1]/form/button/span"
    login_btn = browser.find_by_xpath(login_btn_xpath)
    login_btn.click()

    # If the device needs to be registered, register it
    if browser.is_text_present('unrecognized device', wait_time=25):

        email_confirm_xpath = "/html/body/div/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[3]/div/button"
        email_me_btn = browser.find_by_xpath(email_confirm_xpath)
        email_me_btn.click()

        # sleep time necessary to ensure the email is sent
        time.sleep(30)
        parser = EmailParser(query = 'from:ecuservice AND one-time passcode')
        
        passcode_field_xpath = '//*[@id="mfaCodeInputField"]'
        browser.find_by_xpath(passcode_field_xpath).fill(parser.results[0]['passcode'])
        register_device_xpath = '/html/body/div/div/div[2]/div/div/div[2]/div[2]/div[4]/div[3]/div[1]/button'
        register_device_btn = browser.find_by_xpath(register_device_xpath)
        register_device_btn.click()

    checking_acct_xpath = '//*[@id="accountNameugtEG2lluVkfVc8vahCfrVDyTGH8GZAKo6puiy0IfFg"]'
    checking_acct_btn = browser.find_by_xpath(checking_acct_xpath, wait_time=10)
    checking_acct_btn.click()
    time.sleep(10)

    full_text_body = ""
    full_charge_amount = 0
    for bill in monthly_charge_data.keys():
        transaction_info = get_transaction_info(monthly_charge_data[bill]['bank query'])

        bill = Bill(name = bill + ' bill',
                total = transaction_info[2],
                date = transaction_info[0],
                multiplier = monthly_charge_data[bill]['multiplier'])

        full_text_body += str(bill) + "\n"
        full_charge_amount += bill.amount_to_be_charged


    full_text_body += f"\nTotal = {round( full_charge_amount, 2 )}\n"

request_dict = {'phone': '3038106250', 'message': full_text_body, 'key': api_key}
resp = requests.post('https://textbelt.com/text/', request_dict)

log_info = {
        'run_date': dt.strftime(dt.today(), "%Y-%m-%d %H:%M:%S"),
        'last_run_date': dt.strftime(last_run_date, "%Y-%m-%d %H:%M:%S"),
        'textbelt_response': resp.json(),
        'text': full_text_body
}


LOG_FILE = 'logs.json'
if os.path.exists(LOG_FILE):
    with open(LOG_FILE) as log_file:
        old_logs = json.load(log_file)
        old_logs.update(log_info)
    with open(LOG_FILE,'w') as log_file:
        json.dump(old_logs, log_file, indent = 4)

elif os.path.exists(LOG_FILE) == False:
    with open(LOG_FILE, 'w') as log_file:
        json.dump(log_info, log_file, indent = 4)

# should be last thing to execute
with open(".last_run_date.txt", 'w') as date_file:
    today = dt.strftime(dt.today(), "%Y-%m-%d %H:%M:%S")
    date_file.write(str(today) + "\n")
