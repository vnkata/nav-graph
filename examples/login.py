import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

driver.get("http://phpfusion_v91000.loc/index.php")

formData = {
    # "http://phpfusion_v91000.loc/index.php": {
        "user_name": "admin",
        "user_pass": "12345678",
        "submit_btn_xpath": "//*[@id='login']"
    # }
}
for idx in range(5):
    print (f"Loop #{idx}")

    # find `login` form
    login_form = driver.find_element(By.XPATH, """//*[@id="userinfopanel_login"]""")

    for child_el in login_form.find_elements(By.XPATH, ".//input[@type='text' or @type='password']"):
        print (f"child_el: {child_el}")
        for attr in ['id', 'name']:
            print (f"child_el.get_attribute(attr)={child_el.get_attribute(attr)}")
            if child_el.get_attribute(attr) in formData.keys():
                # child_el._runtime_element.clear()
                print(f"found the child element: {child_el}, use the following value to fill in: {formData[child_el.get_attribute(attr)]}")
                # is_succes = child_el.perform(driver, data=formData[child_el.get_attribute(attr)])
                child_el.send_keys(formData[child_el.get_attribute(attr)])

    # find submit button
    submit_btn = driver.find_element(By.XPATH, """//*[@id="login"]""")
    submit_btn.click()

    # find logout button
    try:
        logout_btn = driver.find_element(By.XPATH, """/html/body/div[2]/div/div/div[2]/div[2]/div/a[5]""")
    except Exception as e:
        logout_btn = driver.find_element(By.XPATH, """/html/body/div[2]/div/div[3]/div/div/a""")

        
    logout_btn.click()

    # print 
print ("Done~")