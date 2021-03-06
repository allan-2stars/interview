import pyautogui
import pandas as pd
import time
from datetime import datetime
import calendar
import pywinauto
from functions.functions_utils import tm_init

from functions.functions_utils import save_as_Excel_analysis


def KPI_FaildedQA():
    if tm_init() is None:
        print("Can't find Templa on your computer")
    else:
        templa = tm_init()[0]
        app = tm_init()[1]


        completedQAWindow = templa.child_window(title='Completed QA Items', control_type='TabItem')
        if not completedQAWindow.exists():
            print('Completed QA Items NOT found?')
            print('Have your open the Complete QA Items Window Tab/Window?')
            print('Exit.')

        else:
            ## start
            print("found the 'Completed QA Items', continue ...")
            completedQAWindow.click_input()
            ##### defined a function for save report into specific forlder repeatively ######

            ########################
            #
            # Setup Excel Sheet
            #
            ########################
            Work_Sheet = 'KPI QA Completed Items' 
            df = pd.read_excel('test.xlsx', sheet_name=Work_Sheet)

            if datetime.now().month - 1 == 0:
                analysis_month = 12
                analysis_year = datetime.now().year - 1
            else:
                analysis_month = datetime.now().month - 1
                analysis_year = datetime.now().year

            analysis_month_string = '01'
            if analysis_month == 1:
                analysis_month_text = 'Jan'
            if analysis_month == 2:
                analysis_month_string = '02'
                analysis_month_text = 'Feb'
            if analysis_month == 3:
                analysis_month_string = '03'
                analysis_month_text = 'Mar'
            if analysis_month == 4:
                analysis_month_string = '04'
                analysis_month_text = 'Apr'
            if analysis_month == 5:
                analysis_month_string = '05'
                analysis_month_text = 'May'
            if analysis_month == 6:
                analysis_month_string = '06'
                analysis_month_text = 'Jun'
            if analysis_month == 7:
                analysis_month_string = '07'
                analysis_month_text = 'Jul'
            if analysis_month == 8:
                analysis_month_string = '08'
                analysis_month_text = 'Aug'
            if analysis_month == 9:
                analysis_month_string = '09'
                analysis_month_text = 'Sep'
            if analysis_month == 10:
                analysis_month_string = str(analysis_month)
                analysis_month_text = 'Oct'
            if analysis_month == 11:
                analysis_month_string = str(analysis_month)
                analysis_month_text = 'Nov'
            if analysis_month == 12:
                analysis_month_string = str(analysis_month)
                analysis_month_text = 'Dec'

            monthName_string = analysis_month_text
            yearName_string = str(analysis_year)

            lastday_analysis_month_string = str(calendar.monthrange(analysis_year, analysis_month)[1])

            dateStartString = '01' + analysis_month_string + yearName_string
            dateEndString = lastday_analysis_month_string + analysis_month_string + yearName_string

            print('starting...')
            print('analysis month: ' + monthName_string + ' analysis year: ' + yearName_string)
            print('analysis month text: ' + analysis_month_text)

            for i in df.index:
                constracts = df['CONTRACTS']
                siteName = df['SITE NAME']
                siteName_string = str(siteName[i])
                site = df['SITE']
                client = df['CLIENT']
                template = df['TEMPLATE']
                filePath = df['PATH']
                fileName = df['FILE_NAME_FAILED_QA_ITEMS']
                status = df['STATUS']

                useContracts = df['USE CONTRACTS']
                useSite = df['USE SITE']
                useClient = df['USE CLIENT']
                useTemplate = df['USE TEMPLATE']

                if status[i] == 'Done':
                    print(siteName_string + ' is Done')
                    continue

                if status[i] == 'Skip':
                    print(siteName_string + ' is Skipped')
                    continue

                if status[i] == 'Stop':
                    print('Stop here')
                    break

                # app.window(title='Change filter', control_type='Button').click_input()
                templa.child_window(title='Change filter', control_type='Button').click_input()
                filterWindow = templa.child_window(title_re='QA Completed Item Filter Detail - *')
                filterWindow.wait('exists', timeout=15)

                ## default filter
                print('Default the Filter.')
                filterWindow.child_window(title='Default criteria').click_input()

                if useTemplate[i] == 'Yes':
                    print('Use Template')
                    ## Use Template Filter
                    filterWindow.child_window(auto_id='cslQATemplate', control_type='Pane').click_input()
                    pyautogui.typewrite(str(int(template[i])))

                    pyautogui.press('tab')

                # ###############################################
                # ############                    ###############
                # ############  Basic Filtering   ###############


                ## filter on date range of audited date
                print('date from ', dateStartString)
                filterWindow.child_window(auto_id='datAuditDateFrom', control_type='Edit').click_input()
                pyautogui.typewrite(dateStartString)
                ##filterWindow.child_window(auto_id='datAuditDateTo', control_type='Edit').click_input()
                pyautogui.press('tab')
                print('date end ', dateEndString)
                pyautogui.typewrite(dateEndString)
                ####
                ## print out the current site
                print('site analytics: ', siteName[i])

                # ## if the site is Special case, use below
                # if siteName_string == 'DAWR Monthly' or siteName_string == 'PMC Monthly':
                #     print('Ignore the failed Items')
                #     ## 
                #     pyautogui.press('right')
                #     pyautogui.press('right')
                #     pyautogui.press('space')
                # # ## ## click on Failed Items button to YES
                # else:
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('tab')
                pyautogui.press('right')
                pyautogui.press('space')


                # ###########   End of Basic Filtering    #########
                # #################################################


                ## change the site filters criteria
                siteFilterCriteria = filterWindow.child_window(title='Site filtering criteria', control_type='TabItem')
                siteFilterCriteria.click_input()


                if useContracts[i] == 'Yes':
                    ## Use Contracts filter
                    print('Use Contracts')
                    filterWindow.child_window(title='Contracts', auto_id='5', control_type='DataItem').click_input()
                    pyautogui.typewrite(str(constracts[i]))
                    pyautogui.press('tab')

                if useSite[i] == 'Yes':
                    ## Use Site Filter
                    print('Use Site')
                    filterWindow.child_window(auto_id='cslSite', control_type='Pane').click_input()
                    pyautogui.typewrite(str(site[i]))
                    pyautogui.press('tab')

                if useClient[i] == 'Yes':
                    ## Use Client Filter
                    print('Use Client')
                    filterWindow.child_window(auto_id='cslClient', control_type='Pane').click_input()
                    pyautogui.typewrite(str(client[i]))
                    pyautogui.press('tab')

                ## check the other tab filtering
                if siteName_string == 'Redcape':    
                    protertyFilterCriteria = filterWindow.child_window(title='Property filtering criteria', control_type='TabItem')
                    protertyFilterCriteria.click_input()
                    ## get the handle of Group filter
                    groupItem = filterWindow.child_window(title='Group', auto_id='2', control_type='DataItem')
                    matchTypeSection = groupItem.child_window(title='Match type', auto_id='3', control_type='ComboBox')
                    valueSection = groupItem.child_window(title='Value', auto_id='1', control_type='ComboBox')

                    ## click and change the filter Equal to ...
                    matchTypeSection.click_input()
                    pyautogui.typewrite('e')  # e, for Equal to
                    pyautogui.press('tab')
                    time.sleep(2)
                    valueSection.click_input()
                    pyautogui.typewrite('r') # filter the site name
                    pyautogui.press('tab')


                # ## Save the filter
                print('Saving the filter ...')
                filterWindow.Save.click_input()
                
                #siteDescriptionTab = completedQAWindow.child_window(title='Site description', control_type='DataItem')
                mainCompletedWindow = templa.child_window(title='Completed QA Items', control_type='Window')
                csmWindow = mainCompletedWindow.child_window(title='CSM', auto_id='56', control_type='ComboBox')
                csmWindow.wait('exists', 180)

                templa.child_window(title='Select format', control_type='Button').click_input()
                filterFormatsWindow = templa.window(title='Filtered List Formats')
                filterFormatsWindow.wait('exists', timeout=15)
                ## type the format name
                filterFormatsWindow.window(title='Description', control_type='ComboBox').click_input()

                ## if the site is Special case, use below
                if siteName_string == 'DAWR Monthly' or siteName_string == 'PMC Monthly' or siteName_string == 'TK MAXX Monthly':
                    pyautogui.typewrite('Special Format')
                    pyautogui.moveRel(-25, 25) 
                    pyautogui.doubleClick() # apply the format
                else:
                    pyautogui.typewrite('Standard Format')
                    pyautogui.moveRel(-25, 25) 
                    pyautogui.doubleClick() # apply the format
                    


                ## read below from excel sheet
                folderName = monthName_string + '-' + yearName_string
                ##
                print('Ready to Export to Excel File ...')
                save_as_Excel_analysis(window=templa, pathName=filePath[i], folderName=folderName, \
                                        fileName=fileName[i], flag='first time save to this folder')
                print(siteName_string + ' is Done.')
                print('#######################')
                print(' ')

