import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from mailtm import Email
import secrets
import string
import numpy as np
import paths
import csv
from datetime import date
import threading # to break out when waiting for the email
import os


class Browser:
    def __init__(self, driver):
        self.options = webdriver.ChromeOptions()
        # to open the browser in incognito mode
        self.options.add_argument("--incognito")
        self.driver = webdriver.Chrome(executable_path=driver, options=self.options)

    def open_page(self, url: str):
        '''Open the given website'''
        self.driver.get(url)

    def close_browser(self):
        '''Close the web browser'''
        self.driver.close()
        self.driver.quit()

    def wait(self, t):
        '''Function to cause a wait for a given t seconds'''
        time.sleep(t)
    
    def random_wait(self, tmin=1, tmax=10, with_fraction=True):
        '''Function to cause a wait for a random time [tmin, tmax]'''
        wait_time = random.randint(tmin, tmax)
        if with_fraction:
            # get a random number [0,1] and round it to 2 decimal pts
            fraction = round(random.uniform(0,1), 2) 
            wait_time += fraction
        
        print("going to wait for {} seconds".format(wait_time))
        time.sleep(wait_time)

    def create_Yahoo_account(self, first_name, last_name, birth_year, email_address, pw):
        #  the website is "https://login.yahoo.com/account/create" (if ever needed)

        # get the required fields 
        fn_field = self.driver.find_element_by_name("firstName")
        ln_field = self.driver.find_element_by_name("lastName")
        br_field = self.driver.find_element_by_name("birthYear")
        e_field  = self.driver.find_element_by_name("userId") 
        pw_field = self.driver.find_element_by_name("password")

        # Set the values of these fields
        fn_field.send_keys(first_name)
        self.random_wait(tmax=4)
        ln_field.send_keys(last_name)
        self.random_wait(tmax=4)
        e_field.send_keys(email_address)
        self.random_wait(tmax=4)
        pw_field.send_keys(pw)
        self.random_wait(tmax=4)
        br_field.send_keys(birth_year)
        self.random_wait(tmax=4)

        submit = self.driver.find_element_by_name("signup")
        submit.click()

    def create_mailtm_email(self, pw):
        print("in create_mailtm function!")
        mail = Email()
        print("Domain:", mail.domain)

        # make new email address
        mail.register(password=pw)
        print("email address:", str(mail.address))

        return mail

    def email_listener(self, mail_obj, interval=1):
        print("in email_listener function")
        # lock = threading.Lock()
        def listener(message):
            print("Recived an email!")
            # print("subject:", message['subject'])
            # print("content: " + message['text'] if message['text'] else message['html'])

            aut_msg_location = "msg.txt"

            # if message['text']:
            with open(aut_msg_location, "w") as file:
                file.write(message['text'])

                # def process_auth_email(self, file_path):
            with open(aut_msg_location, "r") as file:
                lines = [line.rstrip() for line in file]
            
            for line in lines:
                if "Confirm Email" in line:
                    web = line[line.find("(")+1:line.find(")")]
                    break
            
            # Open another tab, put the authentication address there, wait, and close that tab
            js_command = "window.open('{}');".format(web)
            self.driver.execute_script(js_command)
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.wait(1)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

            # Delete the file with the email authentication information
            if os.path.exists(aut_msg_location):
                os.remove(aut_msg_location)
            else:
                print("*** Didn't get/saved authentication email! ***  ")
            
            mail_obj.stop()
            del mail_obj
            # lock.release()

        # lock.acquire()
        # t = threading.Thread(target = mail_obj.start(listener, interval=interval) )
        # t.start()
        mail_obj.start(listener, interval=interval)
        print("wait for the mail")


    def create_Yelp_account(self, first_name, last_name, email, password, zip, bday=None):
        print("in create_Yelp_account function!")
        # Fill in the information
        fn = self.driver.find_element_by_name("first_name")
        fn.send_keys(first_name)
        self.random_wait(tmax=1)

        ln = self.driver.find_element_by_name("last_name")
        ln.send_keys(last_name)
        self.random_wait(tmax=1)

        xpath = "//*[@id='email']"
        em_p = self.driver.find_element("xpath", xpath)
        em_p.send_keys(email) 
        self.random_wait(tmax=3)

        pw = self.driver.find_element_by_name("password")
        pw.send_keys(password)
        self.random_wait(tmax=3)

        zp = self.driver.find_element_by_name("zip")
        zp.send_keys(zip)
        self.random_wait(tmax=3)

        if bday is not None:
            # expecting bday to be in the format mmddyyyy (no other chars or seperators)
            m = bday[:2]
            d = bday[2:4]
            y = bday[4:]
            if m[0] == "0":
                m = m[1]
            if d[0] == "0":
                d = d[1]
            
            # Select the month
            month = self.driver.find_element_by_name("birthdate_m")
            select_m = Select(month)
            select_m.select_by_index(int(m))
            self.random_wait(tmax=2)
            # Select the day
            day = self.driver.find_element_by_name("birthdate_d")
            select_m = Select(day)
            select_m.select_by_index(int(d))
            self.random_wait(tmax=2)
            # Select the year
            year = self.driver.find_element_by_name("birthdate_y")
            select_m = Select(year)
            select_m.select_by_value(y)

        self.random_wait(tmax=3)
        submit = self.driver.find_element_by_id("signup-button")
        submit.click()

    def generate_password(self, length=8):
        # All the english letters (upper & lower) + the 10 digits + special characters
        options = string.ascii_letters + string.digits + "!@#$%^&*"
        # create random password using the char options in the given length
        password = ''.join(secrets.choice(options) for i in range(length))

        return password

    def generate_birthday(self):
        '''Generate a str birthday in the format mmddyyyy. Years range [1955, 2002] '''
        month = random.randint(1,12)
        month = "0" + str(month) if month < 10 else str(month)
        
        day = random.randint(1,28) # to keep it simple with how many days a month
        day = "0" + str(day) if day < 10 else str(day)

        year = str(random.randint(1955,2002))

        bday = month + day + year
        return bday

    def get_random_from_file(self, path):
        '''This function expecting a path to a file. It then loads the file, gets a single line in 
        radom and return the result. Thus expecting the file to be "line separated" (like in the names file)'''

        file = np.loadtxt(path, dtype=str)
        rand_line = random.choice(file)
        # remove whitespace
        rand_line.strip()

        return rand_line

    def log_new_user(self, file_path, e_address, e_password, y_fn, y_ln, y_password, y_zip, y_dob):
        fields = ["email_address", "email_password", "yelp_first_name", "yelp_last_name", "yelp_password",\
                        "yelp_zip_code", "yelp_DoB", "date_created", "last_10_activities_dates", "reviews"]
        new_user = {
                    "email_address": e_address,
                    "email_password": e_password,
                    "yelp_first_name": y_fn,
                    "yelp_last_name": y_ln,
                    "yelp_password": y_password,
                    "yelp_zip_code": y_zip,
                    "yelp_DoB": y_dob,
                    "date_created": str(date.today()),
                    "last_10_activities_dates": None,
                    "reviews": None
                    }

        with open(file_path, "a") as file:
            writer = csv.DictWriter(file, delimiter=',', fieldnames=fields)
            # writer.writeheader() # If needed to write the 'titles'/'fields'
            writer.writerow(new_user)

    def upload_image_yelp_registration(self, img_path):
        bottom_xpath = '//*[@id="super-container"]/div[4]/div[1]/div/div/div[3]/div/div/div[2]/button[2]' # Not sure if correct! 
        print(bottom_xpath)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.find_element("xpath", bottom_xpath).send_keys(img_path)

    def change_ip(self):
        os.system("nordvpn connect")

    def create_new_yelp_user(self, website):
        first_name = self.get_random_from_file(paths.first_name_file_path)
        last_name = self.get_random_from_file(paths.last_name_file_path)
        zip_code = self.get_random_from_file(paths.sd_zips)
        password = self.generate_password(10)
        birthday = self.generate_birthday()
        # might need to put it in try/catch thing and if fails try another 2-3 times (with a different password?)
        email_obj = self.create_mailtm_email(password)
        email_address = email_obj.address

        # Open Yelp
        self.open_page(website)
        self.random_wait(tmax=3)
        
        # Fill in the information (probably a good idea to put in try/catch block)
        self.create_Yelp_account(first_name, last_name, email_address, password, zip_code, birthday)
        # log the information
        self.log_new_user(paths.data, email_address, password, first_name, last_name, password, zip_code, birthday)

        # authenticate Yelp account
        self.random_wait(tmin=2)
        self.random_wait(tmin=10, tmax=15)
        self.email_listener(email_obj, 1)
        print("waiting for email")
        self.random_wait(tmin=25, tmax=30)

        # click the save and continue
        self.driver.find_element_by_id("extra-form-save").click()
        self.random_wait()

        # click to go to the main page
        xpath = '//*[@id="logo"]/a'
        self.driver.find_element("xpath", xpath).click()
        self.random_wait()

        # Click to search in SD
        xpath = '//*[@id="search_location"]'
        address = self.driver.find_element("xpath", xpath)
        address.send_keys(Keys.CONTROL + "a")
        self.random_wait(tmax=1)
        address.send_keys("San Diego, CA")
        address.send_keys(Keys.RETURN)
        self.random_wait(tmax=10)
        
        print("Finished. Closing browser...")
        self.close_browser()


driver_location = paths.driver_location



for i in range(15):
    browser = Browser(driver_location)
    print("create the {} user".format(i+1))
    browser.change_ip()
    browser.wait(3)
    browser.create_new_yelp_user("https://www.yelp.com/signup")
    print("\nclose!\n")
    browser.random_wait(20, 25)
    del browser



    
