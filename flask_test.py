from flask import Flask, request, render_template, redirect, url_for
from selenium import webdriver
import utils.chrome_app

path = r'/Users/andrew/.wdm/drivers/chromedriver/79.0.3945.36/mac64/chromedriver'
driver = webdriver.Chrome(path)
#driver.maximize_window()
browser_name_list = []


app = Flask(__name__)


@app.route('/')
def index():
    '''
    Main page with "run script" and "clear" commands
    '''
    
    return render_template('index.html')


@app.route('/foo', methods=['GET','POST'])
def foo():
    '''
    Text command box for the purposes of testing selenium driver
    '''
    from utils.chrome_app import Chrome_Command, Voice
    '''
    try:
        text = request.form['text']
        print(text)
        if "new tab" in text:
            user_command = Chrome_Command()
            user_command.new_tab()
    except:
        return render_template('textbox.html')
    '''
    voice = Voice()
    voice.initialize_recognition()
    
    return render_template('textbox.html')


@app.route('/foo', methods=['GET','POST'])
def get_command():
    '''
    Executing the command given by text using the chrome_app
    module
    '''
    '''
    text = 'chrome new tab'
    utils.chrome_app.decision_tree(text)
    
    
    #If no dictionary exists, just return the same page
    '''
    
    
    return render_template('textbox.html')
    

@app.route('/boo', methods=['GET', 'POST'])
def boo():
    '''
    Printing and deleting previous selenium commmands
    '''
    
    outfile = open('templates/index.html', 'w')
    outfile.write("""
                  <head>
                  <link rel="stylesheet" type="text/css" href="{{ url_for('static',filename='styles/mainpage.css') }}">
                  </head>
                  <body>
                  <div id="wrapper">
                  <form action="/foo" method="POST"><input type="submit" value="Run&nbsp;Script"></form>
                  <form action="/boo" method="POST"><input type="submit" value="Clear"></form>
                  </div> 
                  </body>
                  """)
    outfile.close()
    textfile = open('templates/text.html', 'w')
    textfile.write("""""")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True, port = 5014)