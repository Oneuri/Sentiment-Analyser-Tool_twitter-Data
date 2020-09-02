import mysql.connector
import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class User:
    
    def signup(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test"
            )
        mycursor = mydb.cursor()
        username = str(input("Enter username : "))
        passwd = str(input("Enter password : "))
        
        sql = "INSERT INTO user (uname, password) VALUES (%s, %s)"
        val = (username, passwd)
        mycursor.execute(sql, val)
        print("User Created")

        mydb.commit()
        
    '''
    def login(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="test"
            )
        mycursor = mydb.cursor()
        username = str(input("Enter username : "))
        passwd = str(input("Enter password : "))
        sql = 
    '''

class SentimentAnalysis:
    def __init__(self):
        self.tweets = []
        self.tweetText = []
    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def clean_tweet(self, tweet):
         return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(str(tweet)))
        self.tweetText.append(self.clean_tweet(str(tweet)).encode('utf-8'))
        
        #print(tweet.text.encode('utf-8'))  #print tweet's text
        
       
        #print("RESULT IN TABULAR FORM")  # print tweet's polarity
        
        
        
        return analysis.sentiment
    
    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, spositive, negative,  snegative, neutral, searchTerm, noOfSearchTerms):
        ppositive = self.percentage(positive, noOfSearchTerms)
                
        pspositive = self.percentage(spositive, noOfSearchTerms)
        pnegative = self.percentage(negative, noOfSearchTerms)
       
        psnegative = self.percentage(snegative, noOfSearchTerms)
        pneutral = self.percentage(neutral, noOfSearchTerms)
        
        labels = ['Positive [' + str(ppositive) + '%]','Strongly Positive [' + str(pspositive) + '%]', 'Neutral [' + str(pneutral) + '%]',
                  'Negative [' + str(pnegative) + '%]','Strongly Negative [' + str(psnegative) + '%]']
        sizes = [ppositive, pspositive, pneutral, pnegative, psnegative]
        colors = ['yellowgreen','darkgreen', 'gold', 'red','lightgreen']
        '''
        print()
        print("Detailed Report: ")
        print(str(ppositive) + "% people thought it was positive")
        
        print(str(pspositive) + "% people thought it was strongly positive")
        print(str(pnegative) + "% people thought it was negative")
        
        print(str(psnegative) + "% people thought it was strongly negative")
        print(str(pneutral) + "% people thought it was neutral")
        '''
        
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        
        plt.show()

    def plotbargraph(self, positive, spositive, negative,  snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive','Strongly Positive', 'Negative','Strongly Negative', 'NEUTRAL']
        sizes = [positive, spositive,  negative, snegative, neutral]
        
        y_pos = np.arange(len(labels))
        
        plt.bar(y_pos, sizes)
        plt.xticks(y_pos, labels)
        plt.ylabel('NUMBER OF TWEETS')
        plt.xlabel('NATURE OF TWEETS')
        
        plt.tight_layout()
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        
        
        plt.show()
        

    def tweets_to_data_frame(self, tweets):

        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['TWEETS'])
    
        '''
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        '''
        return df
    
    

    def DownloadData(self):
            # authenticating
            consumerKey = 'iuuaqlvX2xeL8n6GdfUS51XoR'
            consumerSecret = 'oDzB3S4ntszZwGtyKdEooO5doyNhageceWtHfTvSDlJVU5klpc'
            accessToken = '217120513-D1IhtknTx96Fqvam1zZKGq2BLPtHYSnffyPXMIYi'
            accessTokenSecret = 'EIb8uADCWfxulXnVlnQ0hRRkuBbSUmVnaU791ASWo53yC'
            auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
            auth.set_access_token(accessToken, accessTokenSecret)
            api = tweepy.API(auth)
           
            
            print("1. View tweets by a particular handle.")
            print("2. View top tweets related to a keyword or a hashtag.")
            print("3. Get overall sentiment regarding a topic.")
            print("4. View most retweeted tweets of a keyword.")
            #print("5. View you previous searches.")
            choice = int(input("What would you like to do? "))
            
            if (choice == 1) :
            
                target = input("Enter the Twitter handle name. ")
                print("Getting data for " + target)
                item =api.get_user(target)
                print("name: " + item.name)
                print("screen_name: " + item.screen_name)
                print("statuses_count: " + str(item.statuses_count))
                print("friends_count: " + str(item.friends_count))
                print("followers_count: " + str(item.followers_count))
                NoOfTerms = int(input("Enter how many tweets to search: "))
                tweetts = api.user_timeline(screen_name=target, count=NoOfTerms)



                '''
               
                df = self.tweets_to_data_frame(tweetts)
                print("RESULTS IN TABULAR FORM")                
                print(df.head(NoOfTerms))
'''


                # iterating through tweets fetched
                for tweet in tweetts:
                    #Append to temp so that we can store in csv later. I use encode UTF-8
                    self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                    print ("TWEET: \n" + str(tweet.text.encode('utf-8')))
                    #print (tweet.text.encode('utf-8'))#print tweet's text
                    analysis = TextBlob(tweet.text)
                    print("TWEET ID: " + str(tweet.id))
                    print("TWEET SENTIMENT: " + str(analysis.sentiment))  # print tweet's polarity

                '''
            
                tmp=[]  
          
                # create array of tweet information: username,  
                # tweet id, date/time, text
                
                tweets_for_csv = [tweet.text for tweet in tweetts]
                tweets_for_csv1 = [tweet.id for tweet1 in tweetts]# CSV file created  
                for j in tweets_for_csv1:
                    
          
                    # Appending tweets to the empty array tmp 
                    tmp.append(j)
                    print(tmp)
          
                # Printing the tweets 
                
'''
            elif( choice == 2) :

                # input for term to be searched and how many tweets to search
                searchTerm = input("Enter Keyword/Tag to search about: ")
                NoOfTerms = int(input("Enter how many tweets to search: "))

                # searching for tweets
                tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
                df = self.tweets_to_data_frame(tweets)
                #df['SENTIMENT'] = np.array([self.analyze_sentiment(tweets) for tweet in df['TWEETS']])
                print("RESULTS IN TABULAR FORM")
                
                print(df.head(NoOfTerms))
                '''
                # iterating through tweets fetched
                for tweet in self.tweets:
                    #Append to temp so that we can store in csv later. I use encode UTF-8
                    self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                    print (tweet.text.encode('utf-8'))    #print tweet's text
                    analysis = TextBlob(tweet.text)
                    print(tweet.id)
                    print(analysis.sentiment)  # print tweet's polarity
'''
            elif( choice == 4) :
                print(str(api.retweets(1181227885841002496,[1])))
            
            elif( choice == 3) :

                # input for term to be searched and how many tweets to search
                searchTerm = input("Enter Keyword/Tag to search about: ")
                NoOfTerms = int(input("Enter how many tweets to search: "))

                # searching for tweets
                self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

                # Open/create a file to append data to
                csvFile = open('result.csv', 'a')

                # Use csv writer
                csvWriter = csv.writer(csvFile)


                # creating some variables to store info
                polarity = 0
                positive = 0
                #wpositive = 0
                spositive = 0
                negative = 0
                #wnegative = 0
                snegative = 0
                neutral = 0


                # iterating through tweets fetched
                for tweet in self.tweets:
                    #Append to temp so that we can store in csv later. I use encode UTF-8
                    self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                    print (tweet.text.encode('utf-8'))    #print tweet's text
                    analysis = TextBlob(tweet.text)
                    print(analysis.sentiment)  # print tweet's polarity

                    
                    polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

                    if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                        neutral += 1
                    elif (analysis.sentiment.polarity > 0.0 and analysis.sentiment.polarity <= 0.6):
                        positive += 1
                    elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                        spositive += 1
                    elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= 0):
                        negative += 1
                    elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                        snegative += 1


                # Write to csv and close csv file
                csvWriter.writerow(self.tweetText)
                csvFile.close()
                print(" ")
                print("RESULTS:")
                print(" ")
                print("POSITIVE TWEETS: " + str(positive))
                print("STRONGLY POSITIVE TWEETS: " + str(spositive))
                print("NEUTRAL TWEETS: " + str(neutral))
                print("NEGATIVE TWEETS: " + str(negative))
                print("STRONGLY NEGATIVE TWEETS: " + str(snegative))

                # finding average of how people are reacting
                ppositive = self.percentage(positive, NoOfTerms)
                
                pspositive = self.percentage(spositive, NoOfTerms)
                pnegative = self.percentage(negative, NoOfTerms)
               
                psnegative = self.percentage(snegative, NoOfTerms)
                pneutral = self.percentage(neutral, NoOfTerms)

                # finding average reaction
                polarity = polarity / NoOfTerms

                # printing out data
                
                print()
                print("General Report: ")

                if (polarity == 0):
                    print("Neutral")
                elif (polarity > 0 and polarity <= 0.3):
                    print("Weakly Positive")
                elif (polarity > 0.3 and polarity <= 0.6):
                    print("Positive")
                elif (polarity > 0.6 and polarity <= 1):
                    print("Strongly Positive")
                elif (polarity > -0.3 and polarity <= 0):
                    print("Weakly Negative")
                elif (polarity > -0.6 and polarity <= -0.3):
                    print("Negative")
                elif (polarity > -1 and polarity <= -0.6):
                    print("Strongly Negative")
                """
                print()
                print("Detailed Report: ")
                print(str(positive) + "% people thought it was positive")
                print(str(wpositive) + "% people thought it was weakly positive")
                print(str(spositive) + "% people thought it was strongly positive")
                print(str(negative) + "% people thought it was negative")
                print(str(wnegative) + "% people thought it was weakly negative")
                print(str(snegative) + "% people thought it was strongly negative")
                print(str(neutral) + "% people thought it was neutral")
                """
                print("")
                print("VIEW RESULT IN: ")
                print("1.Pie Chart")
                print("2.Bar Graph")
                
                
                option = int(input("How do you want to see the results?(1/2) "))
                #self.plotPieChart(positive,  spositive, negative,  snegative, neutral, searchTerm, NoOfTerms)
                #self.plotbargraph(positive,  spositive, negative,  snegative, neutral, searchTerm, NoOfTerms)

                
                if(option == 1):
                    print("saasas")
                    self.plotPieChart(positive,  spositive, negative,  snegative, neutral, searchTerm, NoOfTerms)
                    
                elif(option == 2):
                    self.plotbargraph(positive,  spositive, negative,  snegative, neutral, searchTerm, NoOfTerms)
                    
                

                


    



if __name__== "__main__":
    new=User()
    new.signup()
    sa = SentimentAnalysis()
    ch=1
    while True:
        sa.DownloadData()
        print("Press 1 to continue...")
        ch=int(input())
        if ch!=1:
            break

