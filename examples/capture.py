import chromedriver_binary

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement



def interceptor(request, response):  # A response interceptor takes two args
    # print (response.body)
    if response.headers['Content-Length'] is None:
        return
    if response.status_code == 200: #and response.headers.get_content_type() == 'text/html':
        # print (response.body)
        print (response.headers.get_content_type())
        # original_length = int(response.headers['Content-Length'])
        # del response.headers['Content-Length']
        # # print ("headers", response.headers)
        # response.headers['Content-Length'] = str(original_length + len(script_str))
        # # print ("response", response.body)
        # # print ("headers", response.headers)
        # try:
        #     if response.headers['content-encoding'] == 'gzip':
        #         original_body = decompress(response.body)
        #     else:
        #         original_body = response.body
        #     original_body = original_body.decode()
        #     new_body = original_body.replace('<head>', '<head>' + script_str)
        #     # print (new_body)
        #     response.body = new_body.encode()
        #     if response.headers['content-encoding'] == 'gzip':
        #         response.body = compress(response.body)
        # except Exception as e:
        #     # print ("Can not handle  response, eror: ", e)
        #     # print ("headers", response.headers)
        #     # print ("response: ", response.body)
        #     pass

options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)
driver.response_interceptor = interceptor
driver.get("https://github.com/")
print ("Done~")