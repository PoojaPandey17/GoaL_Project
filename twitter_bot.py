# -*- coding: utf-8 -*-

import tweepy
import datetime
import time
import re
import twitter_credentials

class TwitterBot(object):
    
    def __init__(self, user):
        self.api = None
        self.userID = user
        
    def check_cred(self):
        if(self.api is None):
            self.auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
            self.auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
            try:
                self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
                self.api.verify_credentials()
                print("Authentication OK")
                return True
            except tweepy.TweepError:   
                raise PermissionError("Twitter Auth Failed")
                return False
        else:
            #print("API IS ALREADY SET")
            return True
            
    def datetime_from_utc_to_local(self, utc_datetime):
        now_timestamp = time.time()
        offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset
    
    def set_goal_data(self, tweet):
        slist = []
        #print("set_goal_data")
        #print(tweet.full_text)
        name = tweet.full_text.split(":")
        #print(name)
        team_name = name[0]
        time = self.datetime_from_utc_to_local(tweet.created_at)
        
        timestamp = '{0}/{1}/{2} {3}:{4}:{5}'.format(time.day, time.month, time.year, time.hour, time.minute, time.second)
        
        cond1 = rf"{team_name}: (.+?) \(([0-9]+)\) assists:(.+?)Goalie(.+?)\((.+?) ([0-9]+), (.+?) ([0-9]+) - (.+?)\)"
        cond2 = rf"{team_name}: (.+?) - (.+?)\) assists:(.+?)Goalie(.+?)\((.+?) ([0-9]+), (.+?) ([0-9]+) - (.+?)\)"
        
        if(re.match(cond1, tweet.full_text)):
            pat_match= re.search(cond1, tweet.full_text)
            #print("FIRST CONDITION")
            #print(pat_match.group(2))
        elif(re.match(cond2, tweet.full_text)):
            pat_match= re.search(cond2, tweet.full_text)
            #print("SECOND CONDITION")
            #print(pat_match.group(2))
        else:
            print("PLEASE CHECK : TWEET DOESNT MATCH ANY CONDITION")
            
        if(pat_match.group()):
            assist1 = ""
            assist2 = ""
            if(pat_match.group(3)):  
                assists_text = pat_match.group(3).strip()
                #print("ASSISTS")
                #print(assists_text)
                if(assists_text is not None and assists_text != 'none' and assists_text != ''):
                    if(',' in assists_text):
                        ast = re.search(rf"(.+?) \([0-9]+\), (.+?) \([0-9]+\)", assists_text)
                        assist1 = ast.group(1)
                        assist2 = ast.group(2)
                    else:
                        ast= re.search(rf"(.+?) \([0-9]+\)", assists_text)
                        assist1 = ast.group(1)
            goal     = pat_match.group(1)
            team1    = pat_match.group(5)
            score1   = pat_match.group(6)
            team2    = pat_match.group(7)
            score2   = pat_match.group(8)
            gametime = pat_match.group(9)
            #set row to be printed on google sheet 
            slist.extend((timestamp, goal, assist1, assist2, team1, score1, team2, score2, gametime))  
        return slist
        
    
    def get_tweet_timeline(self):
        max_pages = 5
        status = True
        prnt_tweet = []
        tmp = []
        page = 1
        new_since_id = False
        try:
            while page <= max_pages:
        
                if(self.since_id == False):
                    tweet_timelines   =   self.api.user_timeline(screen_name=self.userID,
                                                                     count= 12,
                                                                     tweet_mode = 'extended',
                                                                     include_retweets=True
                                                                    )
                else:
                    tweet_timelines   =   self.api.user_timeline(screen_name=self.userID,
                                                                     count= 20,
                                                                     since_id= self.since_id,
                                                                     tweet_mode = 'extended',
                                                                     include_retweets=True
                                                                    )
                
                if(len(tweet_timelines) > 0):
                    #print("TWEET TIMELINES")
                    #print(tweet_timelines)
                    first = tweet_timelines[0]
                    new_since_id = first.id
                    for item in tweet_timelines:
                        
                        #print(item.full_text)
                        tw_data_list = []
                        #print(self.datetime_from_utc_to_local(item.created_at))
                        tw_data_list = self.set_goal_data(item)
                        if(len(tw_data_list) > 0):
                            tmp.append(tw_data_list)
                            self.since_id = new_since_id
                            page+=1
                        else:
                            print("ERROR WITH TWEETS PATTERN CONDITION!!")
                            status = False
                            break
                else:
                    page = 99
                    #print("No New Tweet Found")
            #print(prnt_tweet)
        except tweepy.TweepError as e:
            print(e.reason)
        for rev_arr in reversed(tmp):
            prnt_tweet.append(rev_arr)
        return prnt_tweet, status
    
    def fetch_tweet(self, since_id):
        self.since_id = since_id
        prnt_tweet = []
        status = False
        if(self.check_cred()):
            if(self.api):
                prnt_tweet, status = self.get_tweet_timeline()
            else:
                print("TWITTER API NOT SET")
        else:
            print("TWITTER CREDENTIALS NOT AUTHENTICATED")
        return prnt_tweet, self.since_id, status
            
        
                
        
        
    
        

