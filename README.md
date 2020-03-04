Goal Project
============


Folder : Goal_Project

files  :    client_secret.json
            twitter_credentials.py
            tweetdata_sheet.py
            twitter_bot.py



=>twitter_bot.py
	This program fetch twitter data of user GoalNHL
        Process the tweet using python regular expression
        Format and push it in list
        List is then passed to "tweetdata_sheet.py"


Run Script : "tweetdata_sheet.py"
=================================

=>This script will update your google sheet with every new tweet data of GoalNHL at 5 minutes interval.

	Following are the prior requirements, that need to be done to run script :
      	1. Get Twitter API keys, Store them in file name "twitter_credentials.py" as following
         	ACCESS_TOKEN = ""
         	ACCESS_TOKEN_SECRET = ""
         	ACCESS_TOKEN_SECRET = ""
         	CONSUMER_SECRET = ""

	2. Create project on Google Drive Spreadsheet. Enable API keys for your project.
           Refer Link to generate client_secret.json file,

           LINK :  "https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html"

           Save "client_secret.json" in python project "Goal_Project" folder.

       3. Most of the python modules are already installed with python.
          For this script you need to install following python packages:
             1. tweepy
             2. gspread
             3. oauth2client
      4. Code is uploaded on "https://github.com/PoojaPandey17/GoaL_Project/"


