# Pierce-College---Transcript-Notifier
When script is ran, will sign into your SIS student portal to check for grade updates and send an email to you if there are any for a specific semester.

# Warning
Will close every instance of firefox running when program closes. Can be undone by commenting line 100, but will cause memory problems.
-Replace line 100 with # os.system("taskkill /f /im firefox.exe")

# Notes 
Depending on the number of classes taken lines 51 will be changed
Depending on the semester and the number of classes taken lines 45 will be swapped with 46 for Fall semester
-Elements are changed on Pierce's website when there is a new semester added

# Instructions
1) Make sure data.py and transcript-RunOnPC.py are in the same folder
2) Will need to install python on computer
3) Download geckodriver ->same file location as where the transcript-RunOnPC.py is located
4) Install selenium -> part of python
5) Make sure firefox is installed -> program will use firefox as the web driver
6) Windows -> the app task scheduler will be able to time when to run the program 
  -Enable the date to be right when Finals start
  -Run however often you want (1 hour is reasonable)
  -Depending on how long your professor takes to grade, set the end date to be when the final grade is posted (2 months to be sure)
