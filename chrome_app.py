import selenium
from selenium import webdriver
import datetime 
from datetime import datetime
import pyaudio
import audioop
import speech_recognition as sr
path = r'C:\Users\Philip\AppData\Local\Programs\Python\Python37-32/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.maximize_window()
browser_name_list = []

class Chrome_Command():
    
    def __init__(self):
        pass
    
    def refresh(self):
        driver.refresh()
        
    def forward(self):
        driver.forward()
    
    def back(self):
        driver.back()
        
    def scroll_down(self):
        driver.execute_script('scrollBy(0,450)')
    
    def scroll_up(self):
        driver.execute_script(('scrollBy(0,-450)'))
        
    def screenshot(self):
        element = driver.find_element_by_tag_name('body')
        element_png = element.screenshot_as_png
        file_name = 'chrome_screenshot{date}.png'.format(date = str(datetime.now())[0:10])
        with open("file_name", "wb") as file:
            file.write(element_png)
            
    def new_tab(self):
        driver.execute_script('window.open()')
        driver.switch_to.window(driver.window_handles[-1])
        
    def close_tab(self):
        driver.execute_script('window.close()')
        driver.switch_to.window(driver.window_handles[-1])
        
    def open_(self, user_input):
        if '.' not in user_input:
            user_input = user_input + '.com'
            driver.get('https://{user_input}'.format(user_input = user_input))
        else:
            driver.get('https://{user_input}'.format(user_input = user_input))
            
    def search(self, user_input): 
        input_all = driver.find_elements_by_xpath('//input')
        input_list = [i.get_attribute('class') for i in input_all]
        link = [i for i in input_list if len(i) > 2 and 'link' not in i]
        driver.find_elements_by_xpath("//input[@class = '{}']".format(link[0]))
        input_box = driver.find_element_by_xpath("//input[@class = '{}']".format(link[0]))
        input_box.send_keys(user_input)
        input_box.submit()
        
    def find_links(self, link_number, browser_name):
        link_all = driver.find_elements_by_xpath('//a')
        link_list = [i.get_attribute('href') for i in link_all]
        link_list_final = [i for i in link_list if i != None and browser_name not in i and 'javascript:void' not in i]
        driver.get(link_list_final[link_number])

class Voice():
        
    def __init__(self):
        self.threshold = 1500
        self.chunk = 1024
        self.fs = 44100
        self.sample_format = pyaudio.paInt16

    def create_recognizer(self):
        return sr.Recognizer()
    
    def get_mic(self):
        return sr.Microphone(device_index = 0)
    
    def get_text(self):
        r = self.create_recognizer()
        with self.get_mic() as source:
            audio = r.listen(source, timeout = 3)
        return r.recognize_google(audio)
        
    def initialize_recognition(self):
        p = pyaudio.PyAudio()
        temp = p.open(format = self.sample_format,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = 1024)
        chunk_count = 0
        user_input = []
        browser_name_list = []
        while True:
            stream = temp
            data = stream.read(self.chunk, exception_on_overflow = False)
            if audioop.rms(data, 2) > self.threshold:
                chunk_count += 1
            else:
                chunk_count = 0
            if chunk_count >= 5:
                try:
                    print('Chrome is listening!')
                    text = self.get_text().lower()
                    print(text)
                    decision_tree(text)
                    if 'goodbye' in text:
                        break
                    else:
                        pass
                except:
                    pass
        return user_input

def decision_tree(text):
    user_command = Chrome_Command()
    word_list = ['first', 'second','third','fourth','fifth','sixth','seventh','eigth','ninth','tenth']
    number_list = [i for i in range(1,11)]
    number_dic = {keys:values for keys, values in zip(word_list, number_list)}
    global browser_name_list
    
    if 'refresh' in text and 'chrome' in text:
        user_command.refresh()
    if 'forward' in text and 'chrome' in text:
        user_command.forward()
    if 'back' in text and 'chrome' in text:
        user_command.back()
    if 'down' in text and 'chrome' in text:
        user_command.scroll_down()
    if 'up' in text and 'chrome' in text:
        user_command.scroll_up()
    if 'screenshot' in text and 'chrome' in text:
        user_command.screenshot()
    if 'new tab' in text and 'chrome' in text:
        user_command.new_tab()
    if 'close tab' in text and 'chrome' in text:
        user_command.close_tab()
    if 'open' in text and 'chrome' in text:
        browser_name = text.split(' ')[-1]
        browser_name_list.append(browser_name)
        user_command.open_(browser_name)
    if 'search' in text or 'look up' in text and 'chrome' in text:
        split_text = text.split(" ")
        text_dic = {key:value for value, key in enumerate(split_text)}
        for keys in text_dic:
            if 'search for' in text and 'chrome' in text:
                temp_index = text_dic['for']
                temp_value = " ".join(split_text[temp_index + 1:])
            if 'for' not in text and 'search' in text and 'chrome' in text:
                temp_index = text_dic['search']
                temp_value = " ".join(split_text[temp_index + 1:])
            if 'look up' in text and 'chrome' in text:
                temp_index = text_dic['up']
                temp_value = " ".join(split_text[temp_index + 1:])
        user_command.search(temp_value)
    for i in word_list:
        if i in text and 'chrome' in text and 'link' in text:
            user_command.find_links(number_dic[i], browser_name_list[-1])    
            
command = Voice()
command.initialize_recognition()