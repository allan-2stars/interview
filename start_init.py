
import pyautogui
from pywinauto.application import Application
import os

def start_init():
    templa_file = r"E:\TCMS_LIVE\Client Suite\TemplaCMS32.exe"
    app = Application(backend='uia').connect(path=templa_file)
    print("Get in Main Window...")
    templa = app.window(title='TemplaCMS  -  Contract Management System  --  TJS Services Group Pty Ltd LIVE')
    templa.wait("exists", timeout=15)
    ## Click on Favourites Menu
    templa.child_window(title="Favourites", control_type="Group").click_input()

    ### the list of title in 'Favourites' menu
    list_favourites = ['Workflow Manager', 'Device Registration', 'Workflow Paths', \
                    'LITE Users', 'Analysis Codes', 'Sites', 'Contracts', 'Contacts']

    ## Open Contract
    for list_title in list_favourites:

        #contractsSubMenu = templa.child_window(title=list_title, control_type="DataItem").click_input()
        #contractsSubMenu.click_input()
        templa.child_window(title=list_title, control_type="DataItem").click_input()

        ## if the window opened need more filter or details to do, use below conditions path
        if list_title == "Sites":
            sitesFilterWindow = templa.window(title_re='Site Filter Detail - *')
            # Wait filter comes out
            sitesFilterWindow.wait('exists', timeout=15)
            sitesFilterWindow.child_window(title="Default criteria").click_input()
            sitesFilterWindow.Save.click_input()
            pyautogui.PAUSE = 10.5
        
        if list_title == "Contracts":
            contractsFilterWindow = templa.window(title_re='Contract Filter Detail -*')
            # Wait filter comes out
            contractsFilterWindow.wait('exists', timeout=15)
            contractsFilterWindow.child_window(title="Default criteria").click_input()
            contractsFilterWindow.Save.click_input()
            pyautogui.PAUSE = 10.5

        if list_title == "Contacts":
            contactsFilterWindow = templa.window(title_re='Contact Filter Detail - *')
            # Wait filter comes out
            contactsFilterWindow.wait('exists', timeout=15)
            contactsFilterWindow.child_window(title="Default criteria").click_input()
            contactsFilterWindow.Save.click_input()
            pyautogui.PAUSE = 5.5
        ### no matter which menu you select, need wait for least 3 seconds
        pyautogui.PAUSE = 3.5