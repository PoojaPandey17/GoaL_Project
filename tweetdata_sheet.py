# -*- coding: utf-8 -*-
import time
import datetime
import gspread
from gspread.models import Cell
from twitter_bot import TwitterBot
from oauth2client.service_account import ServiceAccountCredentials

class SpreadheetUpdater(object):
    
    def __init__(self, file_url):
        self.file_url = file_url
        self.scope = "https://spreadsheets.google.com/feeds"
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        
        self.timestamp = 1
        self.goal      = 2
        self.assist1   = 3
        self.assist2   = 4
        self.team1     = 5
        self.score1    = 6
        self.team2     = 7
        self.score2    = 8
        self.gametime  = 9
    
    
    def gs_cred(self):
        self.gs = gspread.authorize(self.credentials)
        self.sheet = self.gs.open_by_url(self.file_url).sheet1
        
    def write_func(self, tweets_row):
        new_row = 0
        cells = []
        
        for row in range(len(tweets_row)):
            new_row = self.end_row + row + 1
            #print(tweets_row[0][1])
            cells.append(Cell(row=new_row, col = self.timestamp, value = tweets_row[row][0]))
            cells.append(Cell(row=new_row, col = self.goal,      value = tweets_row[row][1]))
            cells.append(Cell(row=new_row, col = self.assist1,   value = tweets_row[row][2]))
            cells.append(Cell(row=new_row, col = self.assist2,   value = tweets_row[row][3]))
            cells.append(Cell(row=new_row, col = self.team1,     value = tweets_row[row][4]))
            cells.append(Cell(row=new_row, col = self.score1,    value = tweets_row[row][5]))
            cells.append(Cell(row=new_row, col = self.team2,     value = tweets_row[row][6]))
            cells.append(Cell(row=new_row, col = self.score2,    value = tweets_row[row][7]))
            cells.append(Cell(row=new_row, col = self.gametime,  value = tweets_row[row][8]))
            
        self.sheet.update_cells(cells)
        self.end_row = new_row
        return 0
    
    #def getListIndex(self. nrow, ncol,row_pos, col_pos):
     #   list_pos = row_pos*ncol + col_pos
    #return(list_pos)
    
    def upd_spreadsheet(self, tweets_row, end_row):
        self.end_row = end_row
        try:
            if(len(tweets_row) > 0):
                print("Writing Row into sheet....")
                self.write_func(tweets_row)
                #self.write_func(tweets_row)
        except:
            print("LOGIN CREDENTIALS NOT WORKING")
            print("TRYING AGAIN TO LOGIN")
            self.gs_cred()
            self.write_func(tweets_row)
        return self.end_row
        
def main():
    since_id = False
    while_status = True
    #FILE LINK GOOGLE SPREADSHEET!!
    
    #file_link = 'https://docs.google.com/spreadsheets/d/1yGrA816qiglw6PpjdyuWfxIfZORaS-zeQB_plcfQxWk/edit#gid=0'
    
    file_link = "https://docs.google.com/spreadsheets/d/12LanzWrCnm48Gq5NRT6RSrJVLVMN2fPz5U9GNSqU-3Y/edit#gid=0"
    tb = TwitterBot("GoalNHL")
    uss = SpreadheetUpdater(file_link)
    uss.gs_cred()
    end_row = 1
    while while_status==True:
        print(datetime.datetime.now())
        try:
            prnt_tweet_rows = []
            prnt_tweet_rows, since_id, twitter_bot_status = tb.fetch_tweet(since_id)
            if(twitter_bot_status):
                
                #print("SINCE ID {}".format(since_id))
                if(len(prnt_tweet_rows) > 0):
                    #print(prnt_tweet_rows)
                    end_row = uss.upd_spreadsheet(prnt_tweet_rows, end_row)
                else:
                    print("No new tweet added to write into sheet!")
                time.sleep(120)
            else:
                print('Twitter BOT Failed!!') 
                break
        except KeyboardInterrupt:
            print('Keyboad Interrupt!!')
            while_status = False
            break
            
if __name__ == '__main__':
    main()
            
            