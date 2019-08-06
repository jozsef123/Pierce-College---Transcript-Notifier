print("program starting...")
import data
from selenium import webdriver          
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys     
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

msg = MIMEMultipart()
msg['From'] = data.gmailUser
msg['To'] = data.receiver
msg['Subject'] = "Grades Updated!"
Active = False
emptyfile = False         

import os
import time       
         
runs = 3
for r in range(runs):
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)   
        driver.get('https://sso.laccd.edu/adfs/ls/idpinitiatedsignon.aspx?loginToRp=epprod.laccd.edu')              #open pierce ssn portal
        UserLogin = driver.find_element_by_id('userNameInput')                                                      #enter username
        UserLogin.send_keys(data.username)
        UserPassword = driver.find_element_by_id('passwordInput')                                                   #enter password
        UserPassword.send_keys(data.password)
        driver.find_element_by_id('passwordInput').send_keys(Keys.ENTER)

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[1]/div/div[2]/div[4]/div/div/ul/li[1]/a')))

        driver.get('https://epprod.laccd.edu/psp/epprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL')

        driver.switch_to.frame("ptifrmtgtframe")

        driver.find_element_by_xpath('//*[@id="SSR_DUMMY_RECV1$sels$1$$0"]').click()            # For 2019 Summer
        #driver.find_element_by_xpath('//*[@id="SSR_DUMMY_RECV1$sels$0$$0"]').click()           # For 2019 Fall
        driver.find_element_by_xpath('//*[@id="DERIVED_SSS_SCT_SSR_PB_GO"]').click()

        name = "CLS_LINK$"
        grade = "STDNT_ENRL_SSV1_CRSE_GRADE_OFF$"
        classesTaken = 1                                                                        # Number of classes taken for that semester
        nameList = [None]*classesTaken
        gradeList = [None]*classesTaken
        gradeMSG = ""
        body = "The grades for your official transcript has been updated."
        for i in range(classesTaken):
            nameID = name + str(i)
            elementName = driver.find_element_by_id(nameID)
            nameList[i] = elementName.text
            gradeID = grade + str(i)
            elementGrade = driver.find_element_by_id(gradeID)
            gradeList[i] = elementGrade.text
            gradeMSG += (elementName.text + ' - ' + elementGrade.text) 

        try:
            myfile = open('Grades.txt','r+')
        except:
            myfile = open('Grades.txt','w')

        with open('Grades.txt','r+') as myfile:
            for j in range(classesTaken):
                if len(open('Grades.txt').readlines()) == 0:
                    myfile.write(nameList[j] + '    ' + gradeList[j] + '\n')
                    Active = True
                for line in myfile:
                    if (nameList[j]) in line:
                        print(nameList[j] + ' has been entered before. No update')
                        break
                    else:
                        myfile.write(nameList[j] + '    ' + gradeList[j] + '\n')
                        Active = True

        msg.attach(MIMEText(body,'html'))
        msg.attach(MIMEText(gradeMSG,'html'))

        if Active:
            print(msg)
            s = smtplib.SMTP('secureus24.sgcpanel.com', 587)
            s.starttls()
            s.login(msg['From'],data.gmailPass)
            s.sendmail(msg['From'],msg['To'],msg.as_string())
            s.quit()  

        driver.quit()
        break
    except:
        pass
    else:
        break
os.system("taskkill /f /im firefox.exe")
print("program done")
