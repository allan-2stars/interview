import pyautogui
import pandas as pd
import time
import csv

import pywinauto
from datetime import datetime
from functions.functions_utils import tm_init

## get the appliation handler from the init function
templa = tm_init()[0]
app = tm_init()[1]

print("Starting...")
## start 
mainContractsTab = templa.child_window(title='Contracts', control_type='TabItem')
mainContractsTab.click_input()
mainContractsWindow = templa.child_window(title='Contracts', control_type='Window')

########################
#
# Setup Excel Sheet
#
########################
sheetLoader = 'Change QA Template' 
df = pd.read_excel('test.xlsx', sheet_name=sheetLoader)
print("Reading Excel...")
for i in df.index:
    siteCode = df['CODE']
    siteName = df['SITE']
    qaTemplate = df['TEMPLATE']
    nextQaDate =  df['NEXT QA']
    status = df['STATUS']
    site_code = str(siteCode[i])

    if status[i] == "Done" or status[i] == "Skip":
        print(site_code + " is Done")
        continue

    if status[i] == "Stop":
        print("Stop here")
        break

    # click on the Code Edit Box
    mainContractsWindow.window(title='Site', control_type='ComboBox').click_input()
    pyautogui.typewrite(site_code)
    pyautogui.moveRel(0, 25) 
    pyautogui.doubleClick() # open the site by double click

    # # open analysis details dialouge window
    contractDetailWindow = app.window(title_re='Contract - *')
    contractDetailWindow.wait('exists', timeout=15)


    # Go to QA tab
    contractDetailWindow.child_window(title='QA', control_type='TabItem').click_input()

    ######################################################
    ## if you want to check the freqency during this process
    ## also you can specify the date for specific frequency
    next_qa_date = ''
    qa_item = ''
    if contractDetailWindow.window(title='30').exists():    
        print("This QA is Monthly currently." + site_code)
        next_qa_date = '01112020'
        qa_item = contractDetailWindow.window(title='30')

    elif contractDetailWindow.window(title='90').exists():     
        print("This QA is Quaterly currently." + site_code)
        next_qa_date = '01112020'
        qa_item = contractDetailWindow.window(title='90')


    elif contractDetailWindow.window(title='7').exists():     
        print("This QA is Weekly currently." + site_code)
        next_qa_date = '19102020'
        qa_item = contractDetailWindow.window(title='7')

    elif contractDetailWindow.window(title='14').exists():     
        print("This QA is Forenightly currently." + site_code)
        next_qa_date = '1910020'
        qa_item = contractDetailWindow.window(title='14')

    elif contractDetailWindow.window(title='365').exists():     
        print("This QA is Yearly currently." + site_code)
        next_qa_date = '01012020'
        qa_item = contractDetailWindow.window(title='365')

    ## if not match above, there must exist an error
    else:
        print("----------------------------------------------")       
        print("This QA is UNKNOWN frequency or QA NOT Exist." + site_code)
        print("Check this please ..." + site_code)
        print("----------------------------------------------")
        contractDetailWindow.Close.click_input()
        continue
    #############################################################
    

    contractDetailWindow.window(title='New version').click_input()

    pyautogui.PAUSE = 2.5
    pyautogui.typewrite('y') ## equivilent to clicking "yes"
    pyautogui.PAUSE = 3.5

    # press the tab of QA
    time.sleep(5)
    contractDetailWindow.child_window(title='QA', control_type='TabItem').click_input()
    qa_item.click_input(double="true")
    print ("openning the qa item...")

    contractDetailWindow.child_window(title='Edit this effective version').click_input()
    pyautogui.PAUSE = 2.5

    contractQAWindow = contractDetailWindow.window(title_re='Contract QA - *')
    contractQAWindow.wait('exists', timeout=15)

    ######################
    #
    # Change QA Template
    #
    ######################
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')
    #pyautogui.typewrite(qaTemplate[i])
    pyautogui.typewrite(qaTemplate[i])
    pyautogui.PAUSE = 2.5

    #contractQAWindow.child_window(title="Any time", control_type="RadioButton").click_input()
    #  contractQAWindow.child_window(auto_id="datNextQA", control_type="Edit").click_input() # next qa edit box
    #  pyautogui.typewrite(next_qa_date)
    pyautogui.press('tab')

    # Save
    contractQAWindow.Accept.click_input()
    contractDetailWindow.window(title='Request approval').click_input()
    pyautogui.PAUSE = 2.5
    pyautogui.typewrite('y') ## equivilent to clicking "yes"
    print(site_code + " updated to Template " + str(qaTemplate[i]))
    time.sleep(50)  
    print("########################")
    print("")
