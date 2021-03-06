#from subprocess import Popen
from pywinauto import Desktop
from pywinauto import Application
import pyautogui
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
#from pywinauto.application import Application
import time
import csv
import os
#import sys
import pywinauto
#from datetime import datetime
from functions.functions_utils import tm_init

## get the appliation handler from the init function
templa = tm_init()[0]
app = tm_init()[1]

## start 
print("Starting...")
mainContractsTab = templa.child_window(title='Contracts', control_type='TabItem')
mainContractsTab.click_input()
mainContractsWindow = templa.child_window(title='Contracts', control_type='Window')

########################
#
# Setup Excel Sheet
#
########################
sheetLoader = 'QA-Recipient' 
df = pd.read_excel('test.xlsx', sheet_name=sheetLoader)

for i in df.index:
    siteName = df['SITE']
    recipient1 = df['RECIPIENT1']
    recipient2 = df['RECIPIENT2']
    recipient3 = df['RECIPIENT3']
    check1 = df['CHECK1']
    check2 = df['CHECK2']
    check3 = df['CHECK3']
    email1 = df['EMAIL1']
    email2 = df['EMAIL2']
    email3 = df['EMAIL3']
    jobTitle1 = df['JOB TITLE1']
    jobTitle2 = df['JOB TITLE2']
    jobTitle3 = df['JOB TITLE3']
    status = df['STATUS']
    #print("Site Name:" + siteName[i])
    #print("CSM: " + csm[i])
    #print("iPad: " + ipad[i])
    if status[i] == "Done" or status[i] == "Skip":
        print(str(siteName[i]) + " is Done")
        continue

    if status[i] == "Stop":
        print("Stop here")
        break

    # click on the Code Edit Box
    mainContractsWindow.window(title='Site', control_type='ComboBox').click_input()
    pyautogui.typewrite(siteName[i])
    pyautogui.moveRel(0, 25) 
    pyautogui.doubleClick() # open the site by double click
    print("starting...")

    # # open analysis details dialouge window
    # #siteDetailWindow = app.window(title_re='Site Detail - *')
    contractDetailWindow = app.window(title_re='Contract - *')
    contractDetailWindow.wait('exists', timeout=25)
    contractDetailWindow.window(title='QA', control_type='TabItem').click_input()

    contractDetailWindow = app.window(title_re='Contract - *')
    contractDetailWindow.wait('exists', timeout=25)
    contractDetailWindow.window(title='QA', control_type='TabItem').click_input()

    # Check if there is QA Items
    # if no qa at all, then no need to change qa recipient
    qaExternalItemTitle = '2 -- External QA -- QA-EXT'
    qaExternalItemTitleOther = '4 -- QA-EXT -- QA-EXT'

    qaExternalItemExists = contractDetailWindow.window(title=qaExternalItemTitle).exists()
    qaExternalItemOtherExists = contractDetailWindow.window(title=qaExternalItemTitleOther).exists()
    print("qa item NORMAL exist: " + str(qaExternalItemExists))
    print("qa item OTHER exist: " + str(qaExternalItemOtherExists))
    
    if  qaExternalItemExists or qaExternalItemOtherExists:
        contractDetailWindow['QA form recipients'].click_input() 
        contractRecipientsWindow = contractDetailWindow.child_window(title_re='Contract Recipients - *')
        contractRecipientsWindow.wait('exists', timeout=15)
        
        #contractRecipientsWindow.wait('exists', timeout=15)
        print("check recipient")
        recipientExitEither = False
        isChecked = False
        recipientsAddingList = [recipient1[i]]
        
        
        checkStateList = [check1[i]]
        emailList = [email1[i]]
        jobTitleList = [jobTitle1[i]]


        # you need add more recipient if recipient2 in excel not empty


        if str(recipient2[i]) != "nan":
            
            recipientsAddingList.append(recipient2[i])

            checkStateList.append(check2[i])
            emailList.append(email2[i])
            jobTitleList.append(jobTitle2[i])
            print('recipient 2 added: ' + str(recipient2[i]))
        
        if str(recipient3[i]) != "nan":

            recipientsAddingList.append(recipient3[i])

            checkStateList.append(check3[i])
            emailList.append(email3[i])
            jobTitleList.append(jobTitle3[i])
            print('recipient 3 added: ' + str(recipient3[i]))


        arrayCount = len(recipientsAddingList)
        print ('now is row: ' + str(i)) 
        for k in range(arrayCount):
            print ('array count: ' + str(arrayCount)+' '+str(k))

            ## Need to check 2 ways around
            ## firstname lastname
            ## lastname firstname
            ## 


            nameArray = str(recipientsAddingList[k]).split(" ")
            nameFirstLast = recipientsAddingList[k]
            nameLastFirst = nameArray[1] + " " + nameArray[0]
            recipientEntryFL = contractRecipientsWindow.window(title=nameFirstLast)
            recipientEntryLF = contractRecipientsWindow.window(title=nameLastFirst)

            print("check name exist or not: " + recipientsAddingList[k])
            recipientExitEither = recipientEntryFL.exists() or recipientEntryLF.exists()
            recipientExitBoth = recipientEntryFL.exists() and recipientEntryLF.exists()

            checkStateOnExcel = str(int(checkStateList[k]))

            ## Recipient Exist in the List First Name Last Name
            
            
            if recipientExitBoth:
                if checkStateOnExcel == "0":
                    print("duplicate name exist: " + nameFirstLast)
                    recipientEntryCheckboxLF = recipientEntryLF.child_window(title="Receive documents?", control_type="CheckBox")
                    recipientEntryCheckboxFL = recipientEntryLF.child_window(title="Receive documents?", control_type="CheckBox")
                    isCheckedLF = recipientEntryCheckboxLF.get_toggle_state()
                    isCheckedFL = recipientEntryCheckboxLF.get_toggle_state()
                    
                    if str(isCheckedFL) != checkStateOnExcel:
                        recipientEntryCheckboxLF.toggle()
                        recipientEntryCheckboxFL.toggle()
                        print("check state CHANGED to: " + checkStateOnExcel)
                    else:
                        print("check state SAME as before: " + checkStateOnExcel)


                if checkStateOnExcel == "1":
                    print("duplicate name exist: " + nameFirstLast)
                    recipientEntryCheckboxLF = recipientEntryLF.child_window(title="Receive documents?", control_type="CheckBox")
                    recipientEntryCheckboxFL = recipientEntryLF.child_window(title="Receive documents?", control_type="CheckBox")
                    isCheckedLF = recipientEntryCheckboxLF.get_toggle_state()
                    isCheckedFL = recipientEntryCheckboxLF.get_toggle_state()
                    
                    # If currently not checked, let Firstname Lastname check
                    if str(isCheckedFL) != checkStateOnExcel:
                        recipientEntryCheckboxFL.toggle()
                        print("First Last, state CHANGED to: " + checkStateOnExcel)

                    # If currently checked, let Firstname Lastname remained
                    if str(isCheckedFL) == checkStateOnExcel:
                        print("First Last, state Same as: " + checkStateOnExcel)

                    # If currently checked, let Lastname Firstname off check
                    if str(isCheckedLF) == checkStateOnExcel:
                        recipientEntryCheckboxFL.toggle()
                        print("duplicate name turned off")

                    # If currently not checked, let Lastname Firstname keep un-checked  
                    if str(isCheckedLF) != checkStateOnExcel:
                        print("duplicated name no need change")

            elif recipientEntryFL.exists():
                print("exist: " + nameFirstLast)
                recipientEntryCheckboxFL = recipientEntryFL.child_window(title="Receive documents?", control_type="CheckBox")
                isCheckedFL = recipientEntryCheckboxFL.get_toggle_state()
                
                print('state in system now: ' + str(isCheckedFL))
                print("  ")
                print('recipient state should be: ' + checkStateOnExcel)
                if str(isCheckedFL) != checkStateOnExcel:
                    recipientEntryCheckboxFL.toggle()
                    print("check state CHANGED to: " + checkStateOnExcel)
                else:
                    print("check state SAME as before: " + checkStateOnExcel)

            ## Recipient Exist in the List, Last Name First Name
            elif recipientEntryLF.exists():
                print("exist: " + nameLastFirst)
                recipientEntryCheckboxLF = recipientEntryLF.child_window(title="Receive documents?", control_type="CheckBox")
                isCheckedLF = recipientEntryCheckboxLF.get_toggle_state()
                
                print('state in system now: ' + str(isCheckedLF))
                print("  ")
                print('recipient state should be: ' + checkStateOnExcel)
                if str(isCheckedLF) != checkStateOnExcel:
                    recipientEntryCheckboxLF.toggle()
                    print("check state CHANGED to: " + checkStateOnExcel)
                else:
                    print("check state SAME as before: " + checkStateOnExcel)
               
            ## Recipient NOT exist, we need to add a new item
            ## but also, need to know if add a CSM or Client
            elif not recipientExitEither and checkStateOnExcel == "0":
                print('recipient not exist, and no need add')
                
                    
            ## If need to add a CSM User
            elif not recipientExitEither and checkStateOnExcel == "1" and jobTitleList[k] == "CSM":
                print('recipient not exist, and need add')
                # click on the add contact button
                contractRecipientsWindow.child_window(title="Add user", control_type="Button").click_input()
                # find the email
                print("adding new CSM user to list...")
                usersSelectWindow = app.window(title='Users')
                usersSelectWindow.wait('exists', timeout=15)
                usersSelectWindow.window(title='Email', control_type='ComboBox').click_input()
                pyautogui.typewrite(str(emailList[k]))
                pyautogui.moveRel(0, 25)
                pyautogui.click()
                usersSelectWindow.Select.click_input()
                # if need more to add, continue above
                usersSelectWindow.Close.click_input()
                

            ## If need to add a Client
            elif not recipientExitEither and checkStateOnExcel == "1" and jobTitleList[k] == "Client":
                # click on the add contact button
                contractRecipientsWindow.child_window(title="Add contact", control_type="Button").click_input()
                # find the email
                print("adding new Contact to list...")
                contactsSelectWindow = app.window(title='Contacts Select')
                contactsSelectWindow.wait('exists', timeout=25)
                contactsSelectWindow.window(title='Email', control_type='ComboBox').click_input()
                pyautogui.typewrite(emailList[k])
                pyautogui.moveRel(0, 25)
                pyautogui.click()
                contactsSelectWindow.Select.click_input()
                # if need more to add, continue above
                contactsSelectWindow.Close.click_input()
                
            else:
                print("something wrong, no conditions is matched")

        # Save
        contractRecipientsWindow.Save.click_input()
        pyautogui.PAUSE = 2.5
        contractDetailWindow.Close.click_input()
        pyautogui.PAUSE = 2.5
        print (siteName[i] + ": Done now")
        print ("######################################")
        print (" ")

                    
    # if no qa at all, the close the window go to next
    else:
        contractDetailWindow.Close.click_input()
        pyautogui.PAUSE = 2.5
        print (siteName[i] + ": No need change due to no QA.")
        print ("######################################")
        print (" ")

    




    


