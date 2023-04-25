import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import os
import paths
from datetime import date

class Browser:
    def __init__(self, driver):
        self.options = webdriver.ChromeOptions()
        # to open the browser in incognito mode
        self.options.add_argument("--incognito")
        self.driver = webdriver.Chrome(executable_path=driver, options=self.options)

    def change_ip(self):
        os.system("nordvpn connect")
    
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

    def get_random_user(self, users_file, file_size=62):
        '''file size is the legnth of the file of the users' information
        Returns a random line from the users' file as a dict object'''
        offset = random.randrange(file_size)
        with open(users_file) as file:
            lines = csv.DictReader(file, delimiter=',')
            for i, line in enumerate(lines):
                if i == offset:
                    return line
    
    def save_user_active(self, line):
        '''save the last 10 times the user was active'''

        activity_list = line["last_10_activities_dates"]
        activity_list = activity_list.split(".")
        if len(activity_list) > 10:
            activity_list.pop(0)
        activity_list.append(date.today())

        activity_str = ""
        for a in activity_list:
            activity_str += a + "."
        
        return activity_str


    def login(self, user, pw):
        '''Assuming https://www.yelp.com/login is open'''
        # att = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', email_field)

        email_field = self.driver.find_element("xpath", '/html/body/div[2]/div[2]/div/div[4]/div[1]/div/div/div[5]/div[1]/form/input[2]') #//*[@id="email"]
        email_field.send_keys(user)
        self.random_wait(tmax=5)
        pw_field = self.driver.find_element("xpath", '/html/body/div[2]/div[2]/div/div[4]/div[1]/div/div/div[5]/div[1]/form/input[3]')
        pw_field.send_keys(pw)
        self.random_wait(tmax=1)
        pw_field.send_keys(Keys.RETURN)
        
        # Waiting for the page to load
        self.random_wait(tmin=10, tmax=15)

    def insert_img(self, img_path):   
        pass     
        self.open_page("https://www.yelp.com/profile")
        img_area_ele = self.driver.find_element("xpath", '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/form/div/div/div/a/img')
        img_src = img_area_ele.get_attribute("src")

        default_img = "https://s3-media0.fl.yelpcdn.com/assets/srv0/yelp_styleguide/bf5ff8a79310/assets/img/default_avatars/user_medium_square.png"
        print(img_src == default_img)

        self.random_wait(tmax=2)
        if img_src == default_img:
        # self.driver.find_element("xpath", '//*[@id="super-container"]/div[2]/div[2]/div/form/div/div/div/a').click()
            self.open_page("https://www.yelp.com/user_photos/add")
            self.random_wait(tmax=2)
            img = self.driver.find_element("xpath", '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/div/button')
            # img.click()
            self.random_wait(tmax=2)
            att = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', img)
            print(att)
            img.send_keys(img_path)

    def do_random_search(self):
        search_options = ["Dog park", "Restoration company", "HVAC", 
        "Constraction", "Mold restoration", "Bars", "Dirt removal", "Water Damage Repair", "Fire Damage Repair",
        "sewage cleanup", "crawl space", "inspector", "Eureka Restoration", "Home Remodeling", "Reconstruction",
        "Home Remodeling Contractors", "home repair", "Flood", "Sewer backup", "Pipe burst", "Insurance claim"]

        search_word = random.choice(search_options)

        #click search bar, clear it and paste word
        search_bar = self.driver.find_element("xpath", '//*[@id="search_description"]')
        search_bar.send_keys(Keys.CONTROL + "a")
        self.random_wait()
        
        search_bar.send_keys(search_word)
        search_bar.send_keys(Keys.TAB)
        self.random_wait(tmax=2)
        search_bar.send_keys(Keys.RETURN)

        self.random_wait(tmin=3)

    def scroll_down(self, percent=1):
        '''How much percent of the page to scroll down. 1 Means all the way to the end'''
        page_h = self.driver.execute_script("return document.body.scrollHeight")
        scroll_down_to = page_h * percent

        i = 0
        while i <= scroll_down_to:
            change = 100
            js_command = "window.scrollTo({},{})".format(i, i+change)
            self.driver.execute_script(js_command)
            i += change
            self.wait(0.1)

        
        self.random_wait()

    def random_activities(self, num_search = 5):
        self.open_page("https://www.yelp.com/login")
        user = self.get_random_user(paths.data, 85)
        email = user["email_address"]
        pw = user["yelp_password"]
        self.login(email, pw)

        for _ in range(num_search):
            self.do_random_search()
            self.random_wait()
            scroll_per = round(random.random(), 2)
            self.scroll_down(scroll_per)
            self.random_wait(tmin=20, tmax=35)




driver_location = paths.driver_location
browser = Browser(driver_location)

while True:
    browser = Browser(driver_location)
    num_search = random.randint(2, 10)
    browser.random_activities(num_search=num_search)
    browser.close_browser()
    browser.change_ip()
    browser.random_wait(tmin=20, tmax=60)
    del browser